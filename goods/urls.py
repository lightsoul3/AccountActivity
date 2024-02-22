from django.urls import path
from storage import settings
from .views import login_user, get_goods, get_good, update_good, delete_good, create_good, get_categories, get_category, update_category, delete_category, create_category, register_user
from django.contrib.auth.views import LogoutView

#added all urls of my views
urlpatterns = [
    path('', get_goods, name='get_goods'),
    path('get_good/<int:pk>/', get_good, name='get_good'),
    path('update_good/<int:pk>/', update_good, name='update_good'),
    path('delete_good/<int:pk>/', delete_good, name='delete_good'),
    path('create_good/', create_good, name='create_good'),

    path('get_categories/', get_categories, name='get_categories'),
    path('get_category/<int:pk>/', get_category, name='get_category'),
    path('update_category/<int:pk>/', update_category, name='update_category'),
    path('delete_category/<int:pk>/', delete_category, name='delete_category'),
    path('create_category/', create_category, name='create_category'),

    path('register/', register_user, name='register'),
    path('login/', login_user, name='login_user'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout_user'), #URL pattern for user logout, using LogoutView to handle logout and redirecting to LOGOUT_REDIRECT_URL.
]
