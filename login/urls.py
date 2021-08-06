from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    
    path('login/', views.login_form, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_form, name="register"),
    
    path('task',views.task_page, name="task"),
    path('task/edit/<int:pk>', views.task_edit, name="edit-task"),
    path('task/delete/<int:pk>', views.task_delete, name="delete-task"),
    
    path('calendar', views.calendar_page, name="calendar")
]
