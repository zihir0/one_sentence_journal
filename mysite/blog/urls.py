from django.urls import path, include
from .views import blog_list, blog_detail, blog_delete, blog_create, blog_update, toggle_like, login_view, logout_view, register_view


urlpatterns = [
    path('create/', blog_create),
    path('api/', include('blog.api_url')),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('<id>/update/', blog_update),
    path ('', blog_list, name='blog_list'),
    path('<id>/', blog_detail),
    path('<id>/delete/', blog_delete),
    path('<int:post_id>/toggle_like/', toggle_like, name='toggle_like'),
] 

