# from django.urls import path , include
# from django.contrib import admin
# from . import views

# urlpatterns = [
#     path('', views.index, name='index'),  # Homepage or dashboard view
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('admin/', admin.site.urls),###
#     path('accounts/', include('django.contrib.auth.urls')),###
#     path('', views.index, name='index'),
#     path('uploads/<str:filename>/', views.download_file, name='download_file'),
#     path('calculate-processing-time/', views.calculate_processing_time, name='calculate_processing_time'),
#     path('search_meter_id/', views.search_meter_id, name='search_meter_id'),
#     path('faq/', views.faq, name='faq'),
#     # path('reports/', views.reports, name='reports')  # Add this line
# ]

from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Homepage or dashboard view
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('uploads/<str:filename>/', views.download_file, name='download_file'),
    path('calculate-processing-time/', views.calculate_processing_time, name='calculate_processing_time'),
    path('search_meter_id/', views.search_meter_id, name='search_meter_id'),
    # Uncomment or remove as needed
    # path('reports/', views.reports, name='reports'),  # Optional, if you need the reports page
]