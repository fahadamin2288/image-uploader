from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('image/<int:id>/', views.image_detail, name='image_detail'),
    path('image/<int:id>/delete/', views.delete_image, name='delete_image'),
    path('image/<int:id>/update/', views.update_image, name='update_image'),
]
