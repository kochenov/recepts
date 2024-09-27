from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category
import random
from django.shortcuts import render, redirect
from .forms import RecipeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def home(request):
    recipes = Recipe.objects.all()
    random_recipes = random.sample(list(recipes), 5) if recipes.count() >= 5 else recipes
    return render(request, 'home.html', {'recipes': random_recipes})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу после успешной регистрации
    else:
        form = UserCreationForm()  # Возвращаем пустую форму при GET-запросе
    return render(request, 'registration/register.html', {'form': form})

@login_required  # Убедитесь, что только авторизованные пользователи могут добавлять рецепты
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)

            # Назначаем текущего пользователя в качестве автора рецепта
            recipe.author = request.user

            # Проверяем, была ли введена новая категория
            new_category_name = form.cleaned_data.get('new_category')
            if new_category_name:
                # Создаем новую категорию, если она была введена
                new_category, created = Category.objects.get_or_create(name=new_category_name)
                recipe.save()  # Сохраняем рецепт перед добавлением категорий
                recipe.category.add(new_category)
            else:
                # Если выбраны существующие категории, добавляем их
                form.save_m2m()

            recipe.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

