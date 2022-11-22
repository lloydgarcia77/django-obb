from django.urls import path
from obb_app import views
from django.views.generic import TemplateView

app_name = "obb_app"

urlpatterns = [
    path('', views.index, name='index'),   
    path('booking/search-results/', views.search_results, name='search_results'),   
    path('step/1', views.step1, name='step1'),   
    path('step/2', views.step2, name='step2'),   
    path('step/3', views.step3, name='step3'),   
    path('step/4', views.step4, name='step4'),   
    path('step/5', views.step5, name='step5'),   
    path('step/final', views.step_final, name='step_final'),   
    path('update-reference-id/', views.update_ref_id, name='update_ref_id'),   

    # NOTE: Admin

    path('administrator/index/', views.administrator_index, name='administrator_index'),   
    path('administrator/schedules/', views.administrator_schedules, name='administrator_schedules'),   
    path('administrator/schedules/manage/<uuid:id>/', views.administrator_schedules_manage, name='administrator_schedules_manage'),   
]