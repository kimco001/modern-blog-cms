from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def social_meta(post, request):
    url = request.build_absolute_uri()
    image = post.featured_image.url if post.featured_image else ''
    
    return format_html('''
        <meta name="description" content="{}">
        <meta name="keywords" content="{}">
        
        <!-- Open Graph -->
        <meta property="og:title" content="{}">
        <meta property="og:description" content="{}">
        <meta property="og:image" content="{}">
        <meta property="og:url" content="{}">
        <meta property="og:type" content="article">
        
        <!-- Twitter -->
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="{}">
        <meta name="twitter:description" content="{}">
        <meta name="twitter:image" content="{}">
    ''', 
    post.get_meta_description(),
    ', '.join([tag.name for tag in post.tags.all()]),
    post.get_meta_title(),
    post.get_meta_description(),
    image,
    url,
    post.get_meta_title(),
    post.get_meta_description(),
    image)