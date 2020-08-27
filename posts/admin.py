from django.contrib import admin

from .models import Post, Group, Comment, Follow


class PostAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("text", "pub_date", "author")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("text",)
    # добавляем возможность фильтрации по дате
    list_filter = ("pub_date",)


# при регистрации модели Post источником конфигурации для неё назначаем класс PostAdmin
admin.site.register(Post, PostAdmin)


class GroupAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    list_display = ("title", "slug")
    search_fields = ("title",)
    list_filter = ("slug",)


admin.site.register(Group, GroupAdmin)


class CommentsAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    list_display = ("author", "text")
    search_fields = ("text",)
    list_filter = ("created",)


admin.site.register(Comment, CommentsAdmin)


class FollowAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    list_display = ("author", "user")
    search_fields = ("user",)
    list_filter = ("user",)


admin.site.register(Follow, FollowAdmin)
