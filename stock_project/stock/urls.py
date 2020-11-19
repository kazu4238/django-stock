from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('list_edit',views.add_stock,name="list_edit"),
    path('delete/<stock_id>',views.delete,name="delete"),
    path('plot/',views.get_svg, name='plot'),

]