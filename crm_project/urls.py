from django.contrib import admin
from django.urls import path, include
from contacts import views as contacts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('contacts.urls')),
    path('', contacts_views.index, name='index'),
    path('clients/', contacts_views.clients_list, name='clients_list'),
    path('tasks/', contacts_views.tasks_list, name='tasks_list'),
    path('deals/', contacts_views.deals_list, name='deals_list'),
    path('products/', contacts_views.products_list, name='products_list'),
    path('reports/', contacts_views.reports, name='reports'),
    path('download-data/', contacts_views.download_data, name='download_data'),
]
