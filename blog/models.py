from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    status_choices = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    )
    title = models.CharField(max_length=250, unique=True, verbose_name='Заголовок')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author', verbose_name='Автор')
    body = models.TextField(verbose_name='Текст')
    publish = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    status = models.CharField(max_length=10,
                              choices=status_choices,
                              default='draft',
                              verbose_name='Статут публикации')
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='author_comment',
        verbose_name='Автор комментария')
    email = models.EmailField(max_length=250, verbose_name='E-mail')
    body = models.TextField(verbose_name='Сообщение')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Comment by {self.author.name} on {self.post}'
