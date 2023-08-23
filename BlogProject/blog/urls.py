from django.urls import path
from . import views

urlpatterns=[
    # path('', views.post_list, name="post_list"),
    path('', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('blog/', views.blog_view, name='blog'),
    path('verify_otp/', views.verify_otp_view, name='verify_otp'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('update/<int:post_id>/', views.update_post_view, name='update_post'),
    path('delete/<int:post_id>/', views.delete_post_view, name='delete_post'),
    path('post/<int:post_id>/', views.post_detail_view, name='post_detail'),
   

]