from django.contrib import admin
from .models import Comment
from django.utils.html import format_html
from django.utils import timezone
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RangeDateFilter   # ← Corrected import

from .models import Category, Post, PostImage
from .models import Profile


class PostImageInline(TabularInline):
    model = PostImage
    extra = 1
    fields = ['image', 'caption']
    max_num = 10


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = [
        'title', 
        'author', 
        'status_colored', 
        'category', 
        'featured_image_preview',
        'views',
        'published_at',
        'created_at'
    ]
    
    list_filter = [
        'status', 
        'category', 
        'is_featured',
        ('published_at', RangeDateFilter),   # ← Fixed here
        'created_at',
    ]
    
    search_fields = ['title', 'content', 'meta_title', 'meta_description']
    prepopulated_fields = {'slug': ('title',)}
    
    autocomplete_fields = ['author', 'category']
    inlines = [PostImageInline]
    
    actions = ['make_published', 'make_draft', 'mark_featured']

    def status_colored(self, obj):
        colors = {
            'published': 'success',
            'draft': 'warning',
            'scheduled': 'info',
        }
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            colors.get(obj.status, 'default'),
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'

    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" width="80" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.featured_image.url
            )
        return "-"
    featured_image_preview.short_description = 'Image'

    def make_published(self, request, queryset):
        queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, "Selected posts have been published.")
    make_published.short_description = "Mark selected as Published"

    def make_draft(self, request, queryset):
        queryset.update(status='draft')
        self.message_user(request, "Selected posts have been moved to Draft.")
    make_draft.short_description = "Mark selected as Draft"

    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, "Selected posts marked as Featured.")
    mark_featured.short_description = "Mark as Featured"

    fieldsets = (
        ("Basic Information", {
            'fields': ('title', 'slug', 'author', 'category', 'tags', 'status')
        }),
        ("Content", {
            'fields': ('content', 'excerpt', 'featured_image')
        }),
        ("SEO", {
            'fields': ('meta_title', 'meta_description', 'og_image'),
            'classes': ('collapse',)
        }),
        ("Publishing", {
            'fields': ('published_at', 'is_featured', 'views'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['views']
        return []


admin.site.register(PostImage)


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ['name', 'post_link', 'short_body', 'created_at', 'active']
    list_filter = ['active', 'created_at', 'post']
    search_fields = ['name', 'email', 'body', 'post__title']
    list_editable = ['active']
    actions = ['approve_comments', 'reject_comments']
    
    fieldsets = (
        ("Comment Info", {
            'fields': ('post', 'name', 'body', 'parent')
        }),
        ("Status", {
            'fields': ('active',),
        }),
    )

    def post_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.post.get_absolute_url(), obj.post.title)
    post_link.short_description = 'Post'

    def short_body(self, obj):
        return obj.body[:80] + "..." if len(obj.body) > 80 else obj.body
    short_body.short_description = 'Comment'

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
        self.message_user(request, f"{queryset.count()} comments approved successfully.")
    approve_comments.short_description = "✅ Approve selected comments"

    def reject_comments(self, request, queryset):
        queryset.update(active=False)
        self.message_user(request, f"{queryset.count()} comments rejected.")
    reject_comments.short_description = "❌ Reject selected comments"



@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ['user', 'bio_short']
    search_fields = ['user__username', 'user__email', 'bio']
    
    def bio_short(self, obj):
        return obj.bio[:80] if obj.bio else "-"
    bio_short.short_description = 'Bio'
