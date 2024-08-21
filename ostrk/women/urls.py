from django.conf.urls.static import static
from django.urls import path

from ostrk import settings
from . import views

app_name = 'women'

urlpatterns = [
    path('', views.index, name='index'),
    path('cats/<int:cat_id>', views.categories, name='cats'),
    path('about/', views.about, name='about'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('filter/<slug:slug>/', views.filter_by_category, name='filter_by_category'),
    path('favorites/', views.favorites, name='favorites'),
    path('add/favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove/favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('search/', views.search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
