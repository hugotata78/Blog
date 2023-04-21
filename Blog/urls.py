from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='home_page'),
    path('post/<slug:slug>', views.PostView.as_view(), name='post'),
    path('featured/', views.FeaturedPostListView.as_view(), name='featured'),
    path('category/<slug:slug>', views.CategoryListView.as_view(), name='category'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('order/<str:order>', views.SortListView.as_view(), name='order'),
]
