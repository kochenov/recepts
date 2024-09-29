from django import forms
from .models import Recipe, Category


class RecipeForm(forms.ModelForm):
    new_category = forms.CharField(required=False, label="Новая категория",
                                   help_text="Добавьте новую категорию, если её ещё нет")
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False, label="Категория")

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'cooking_time', 'image', 'category']

    def clean(self):
        cleaned_data = super().clean()
        new_category = cleaned_data.get("new_category")
        category = cleaned_data.get("category")

        if not category and not new_category:
            raise forms.ValidationError("Необходимо выбрать существующую категорию или добавить новую.")

        return cleaned_data
