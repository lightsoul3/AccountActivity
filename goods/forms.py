from django import forms
from .models import Category, Good
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# careted form for Categories used for create and adit
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

# careted form for Good Item used for create and adit and added validayion of image size
class GoodForm(forms.ModelForm):
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes

    class Meta:
        model = Good
        fields = ['name', 'price', 'description', 'image', 'category'] 


# This method cleans the 'image' field, ensuring it does not exceed the maximum file size limit.
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > self.MAX_IMAGE_SIZE:
                raise ValidationError("The maximum file size is 10MB")
        return image

#Form fow searching by name    
class SearchForm(forms.Form):
    search_query = forms.CharField(label='', max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Enter name ...'}))


#Registration form
class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

