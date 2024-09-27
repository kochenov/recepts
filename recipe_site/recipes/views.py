from django.shortcuts import render, get_object_or_404
from .models import Recipe
import random
from django.shortcuts import render, redirect
from .forms import RecipeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def home(request):
    recipes = Recipe.objects.all()
    random_recipes = random.sample(list(recipes), 5) if recipes.count() >= 5 else recipes
    return render(request, 'home.html', {'recipes': random_recipes})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RecipeForm()
    return render(request, 'add_recipe.html', {'form': form})

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
