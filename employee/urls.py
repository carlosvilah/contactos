from django.urls import path
from employee import views


urlpatterns = [
    path("",views.EmployeeListView.as_view(),name='employee_list'),
    path("<int:pk>/details/", views.employee_detail,name='employee_detail'),
]