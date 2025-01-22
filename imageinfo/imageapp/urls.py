from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('image/<int:id>/', views.image_detail, name='image_detail'),
    path('image/<int:id>/delete/', views.delete_image, name='delete_image'),
    path('image/<int:id>/update/', views.update_image, name='update_image'),
    path("reset-password/", views.request_password_reset, name="password_reset_request"),
    path("reset-password/<str:token>/", views.reset_password, name="password_reset"),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:image_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:image_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
