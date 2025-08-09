"""
URL configuration for graph_explorer project.

The `urlpatterns` list routes URLs to views.py. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views.py
    1. Add an import:  from my_app import views.py
    2. Add a URL to urlpatterns:  path('', views.py.home, name='home')
Class-based views.py
    1. Add an import:  from other_app.views.py import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('plugins', views.plugins, name="plugins"),

    path('generate-graph/', views.generate_graph, name="graph"),
    path('change-visualizer/', views.visualizer_change, name='change-visualizer'),
    path('change-data-source/', views.data_source_change, name='change-data-source'),
    path('upload-data-file/', views.data_file_upload, name='upload-data-file'),
    path('execute-command/', views.execute_command, name='execute-command'),
    path('filter/', views.filter, name='filter'),
]
