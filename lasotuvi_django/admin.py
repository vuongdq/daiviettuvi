from django.contrib import admin
from .models import Category, Tag, News, NewsImage, Course, Lesson

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_published', 'is_featured', 'views_count', 'created_at')
    list_filter = ('is_published', 'is_featured', 'category', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags', 'related_news')
    inlines = [NewsImageInline]
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ('news', 'caption', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('news__title', 'caption')
    ordering = ('-uploaded_at',)

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    ordering = ('order',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'price', 'is_published', 'is_featured', 'enrollment_count', 'rating', 'created_at')
    list_filter = ('is_published', 'is_featured', 'category', 'level', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LessonInline]
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'is_free', 'duration', 'created_at')
    list_filter = ('is_free', 'course', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('course', 'order') 