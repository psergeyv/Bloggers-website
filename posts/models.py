from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Group(models.Model):
    title = models.CharField(max_length=200,default=None)
    slug = models.SlugField(max_length=100, unique=True,default=None)
    description = models.TextField()
    def __str__(self):
        return self.title

class Post(models.Model):
    text = models.TextField(verbose_name = "Текст поста")
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post",verbose_name = "Автор")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_posts", blank=True, null=True, verbose_name = "Группа")
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

class Comment(models.Model):  
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments_post", blank=True, null=True, verbose_name = "Пост")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment",verbose_name = "Автор коментария")
    text = models.TextField(verbose_name = "Комментарий")
    created = models.DateTimeField("date comment", auto_now_add=True)

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower",verbose_name = "Подписчик")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following",verbose_name = "Автор постов")