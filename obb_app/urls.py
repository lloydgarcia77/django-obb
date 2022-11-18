from django.urls import path
from obb_app import views
from django.views.generic import TemplateView

app_name = "obb_app"

urlpatterns = [
    path('', views.index, name='index'),   
    path('step/1', views.step1, name='step1'),   
    path('step/2', views.step2, name='step2'),   
    path('step/3', views.step3, name='step3'),   
    path('step/4', views.step4, name='step4'),   

    # NOTE: Admin

    path('administrator/index/', views.administrator_index, name='administrator_index'),   
]