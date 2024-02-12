from django import forms
from .models import Category, Good
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class GoodForm(forms.ModelForm):
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes

    class Meta:
        model = Good
        fields = ['name', 'price', 'description', 'image', 'category']

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > self.MAX_IMAGE_SIZE:
                raise ValidationError("The maximum file size is 10MB")
        return image
