from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_file, name='upload'),
    path('detail/<int:file_id>/', views.detail, name='detail'),
    path('buy/<int:file_id>/', views.buy_file, name='buy'),
    path('transfer/<int:file_id>/', views.transfer_ownership, name='transfer'),

    # 添加这个：
    path('registration/', include('django.contrib.auth.urls')),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('search/', views.search_transactions, name='search_transactions'),

]
