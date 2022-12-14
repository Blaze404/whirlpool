from . import views
from django.urls import path

app_name = 'whirlpool_website'


urlpatterns = [
    path('', views.index, name='index'),
    path('create_user/', views.create_user, name="create_user"),
    path('login/', views.login, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('inventory/', views.inventory, name="inventory"),
    path("add_inventory/", views.add_inventory, name="add_inventory"),
    path("remove_inventory/", views.remove_inventory, name="remove_inventory"),
    path("add_transaction/", views.add_transaction, name="add_transaction"),
    path("return_inventory/", views.return_inventory, name="return_inventory"),
    path('show_all_users/', views.show_all_users, name='show_all_users'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/dashboard/', views.dashboard_api, name='dashboard_api'),
    path('api/add_inventory/', views.add_inventory_api, name='add_inventory_api'),
    path('api/add_employee/', views.add_employee_api, name='add_employee_api'),
    path('api/available_quantity/', views.available_quantity_api, name='available_quantity_api'),
    path('api/add_transaction/', views.add_transaction_api, name='add_transaction'),
    path('api/inventory/', views.inventory_api, name='inventory_api'),
    path('api/return_inventory/', views.return_inventory_api, name='return_inventory_api'),
    path('api/create_user/', views.create_user_api, name='create_user_api')
]