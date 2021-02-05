from django.urls import path
from . import views

app_name = 'leads'
urlpatterns = [
    path('', views.LeadListView.as_view(), name='homepage'),
    path('lead/<int:pk>/', views.LeadDetailView.as_view(), name='lead-detail'),
    path('create/', views.LeadCreatelView.as_view(), name='lead-create'),
    path('update/<int:pk>/', views.LeadUpdateView.as_view(), name='lead-update'),
    path('delete/<int:pk>/', views.LeadDeleteView.as_view(), name='lead-delete'),
    path('assign-agent/<int:pk>/',
         views.AssignAgentView.as_view(), name='assign-agent'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('assign-agent/<int:pk>/',
         views.AssignAgentView.as_view(), name='assign-agent'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(),
         name='category-detail'),
    path('lead-category/<int:pk>/', views.LeadCategoryUpdateView.as_view(),
         name='lead-category-update'),
]
