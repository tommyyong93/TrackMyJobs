from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('create/',views.CreateJob.as_view(),name='create'),
    path('joblist/',views.JobList.as_view(),name='list'),
    path('dashboard/',views.JobDashboard.as_view(),name='dashboard'),
    path('plots/',views.JobPlots.as_view(),name='plots'),
    path('<int:pk>/',views.JobDetail.as_view(),name='detail'),
    path('<int:pk>/edit/',views.JobUpdate.as_view(),name='job_edit'),
    path('<int:pk>/remove/',views.JobDelete.as_view(),name='job_remove'),
    path('filter/',views.job_list_filter,name='filter'),
]
