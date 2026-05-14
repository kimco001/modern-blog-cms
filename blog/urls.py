from django.urls import path
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemaps import PostSitemap

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('categories/', views.category_list, name='all_categories'),
    path('author/<str:username>/', views.author_profile, name='author_profile'),
    path('authors/', views.authors_list, name='authors_list'),
    # New Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': {'posts': PostSitemap}}, name='sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt'),
]