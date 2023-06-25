from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'weblog'
urlpatterns = [
                  path('', views.index, name='index'),
                  path('new_post/', views.new_post, name='new_post'),
                  path('post/<int:pk>/', views.post_detail, name='post_detail'),
                  path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
                  path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
                  path('comment/<int:pk>/', views.comment, name='comment'),
                  path('signup/', views.signup, name='signup'),
                  path('login/', views.login_view, name='login'),
                  path('logout/', views.logout_view, name='logout'),
                  path('api/fetch_users', views.fetch_users, name='count'),
              ]

