from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category
import random
from django.shortcuts import render, redirect
from .forms import RecipeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView


def home(request):
    all_recipes = list(Recipe.objects.all())  # Получаем все рецепты
    random_recipes = random.sample(all_recipes, min(len(all_recipes), 5))  # Выбираем случайные рецепты
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
            recipe.save()  # Сохраняем рецепт, чтобы получить его ID

            # Проверяем, была ли введена новая категория
            new_category_name = form.cleaned_data.get('new_category')
            if new_category_name:
                # Создаем новую категорию, если она была введена
                new_category, created = Category.objects.get_or_create(name=new_category_name)
                recipe.category.add(new_category)  # Добавляем новую категорию к рецепту
            else:
                # Если выбраны существующие категории, добавляем их
                form.save_m2m()  # Сохраняем связь с существующими категориями

            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})


@login_required  # Убедитесь, что только авторизованные пользователи могут редактировать рецепты
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe.pk)  # Измените 'pk' на 'recipe_id'
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/edit_recipe.html', {'form': form, 'recipe': recipe})


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 5  # Число рецептов на одной странице

    def get_queryset(self):
        # Получаем все рецепты по умолчанию
        queryset = Recipe.objects.all()

        # Получаем категорию из параметров запроса
        category_name = self.request.GET.get('category')
        if category_name:
            # Фильтруем рецепты по категории, если она передана
            queryset = queryset.filter(category__name=category_name)

        return queryset

    def get_context_data(self, **kwargs):
        # Добавляем дополнительные данные в контекст
        context = super().get_context_data(**kwargs)

        # Добавляем все категории для фильтрации в шаблон
        context['categories'] = Category.objects.all()

        # Добавляем текущую категорию, чтобы она была активной в фильтре
        context['current_category'] = self.request.GET.get('category')

        return context
