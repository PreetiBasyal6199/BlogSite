from .views import SearchResult, UserRegisterView, LoginView, Home, UserLogoutView, BlogEditView, blogPost, viewBlog, BlogDetailView, DeleteBlogView
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('', Home),
    path('register/', UserRegisterView, name='register'),
    path('login/', LoginView, name='login'),
    path('logout/', UserLogoutView, name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="BLOGAPP/PasswordReset.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="BLOGAPP/PasswordResetSent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="BLOGAPP/PasswordResetConform.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="BLOGAPP/PasswordResetComplete.html"), name='password_reset_complete'),
    path('post_blog/', blogPost, name='blog_post'),
    path('view_blog/', viewBlog, name='view_blog'),
    path('blog/<int:pk>/', BlogDetailView, name='blog-detail'),
    path('edit/<int:pk>/', BlogEditView, name='blog-edit'),
    path('delete/<int:pk>/', DeleteBlogView, name='blog-delete'),
    path('search_blog/', SearchResult, name='search_blog'),


]
