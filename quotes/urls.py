from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name= "home1"),
    path('about/', views.about, name= "about"),
    path('add_stock/', views.add_stock, name = "add_stock"),
    path('delete/<stock_id>', views.delete, name="delete"),
    path('delete_stock/', views.delete_stock, name = "delete_stock"),
    path('news/', views.news, name = "news"),
    path('profile/', views.profile, name="profile"),
    path('profile/edit',views.edit,name='edit'),
    path('autocomplete/ticker/', views.TickerAutocomplete.as_view(), name = 'ticker-autocomplete'),
    path('graph/<ticker>', views.graph, name = 'graph'),
    path('test/',views.test)
]