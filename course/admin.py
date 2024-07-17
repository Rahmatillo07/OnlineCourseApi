from django.contrib import admin

from .models import Course, Topic, Video, Comment, LikeDislike,User


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1


class TopicInline(admin.StackedInline):
    model = Topic
    extra = 1


class VideoInline(admin.StackedInline):
    model = Video
    extra = 1


class LikeDislikeInline(admin.StackedInline):
    model = LikeDislike
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created']
    list_editable = ['created']
    search_fields = ['id', 'title']
    list_display_links = ['title']
    list_filter = ['title']
    inlines = [CommentInline,TopicInline,LikeDislikeInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'course']
    list_editable = ['course']
    search_fields = ['id', 'title']
    list_display_links = ['title']
    list_filter = ['title']
    inlines = [VideoInline]

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','user_role']
    list_editable = ['user_role']
    search_fields = ['username']
    list_display_links = ['username']
    list_filter = ['username']