from django.urls import path
from awsapp import views

urlpatterns=[
    path('',views.index),
    path('Create_Bucket',views.Create_Bucket),
    path('LIST_BUCKET',views.LIST_BUCKET),
    path('Delete_Bucket',views.Delete_Bucket),
    path('Add_File',views.Add_File),
    path('Delete_File',views.Delete_File),
    path('copy_file',views.copy_file),
    path('move_file',views.move_file)
]