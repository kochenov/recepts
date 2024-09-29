from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import RecipeListView
from .views import edit_recipe
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
                  path('recipe/edit/<int:pk>/', edit_recipe, name='edit_recipe'),
    path('recipe/add/', views.add_recipe, name='add_recipe'),
    # Маршруты для авторизации и выхода
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
                  path('recipes/', RecipeListView.as_view(), name='recipe_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
