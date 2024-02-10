from django import forms
from webapp.models import Project, Review, Category


class ProjectForm(forms.ModelForm):
    new_category = forms.CharField(max_length=100, required=False, label='Новая категория')

    class Meta:
        model = Project
        fields = ('title', 'description', 'category', 'price')
        widgets = {'category': forms.CheckboxSelectMultiple}
        error_messages = {
            'title': {
                'required': 'Please enter',
                'min_length': 'Заголовок слишком короткий'
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        if title == description:
            raise forms.ValidationError('Заголовок и Контент не могут быть одинаковые')
        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text',)


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Найти')
