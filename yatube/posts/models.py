from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Community model."""
    title = models.CharField('title', max_length=200)
    slug = models.SlugField('group name', unique=True)
    description = models.TextField('description')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'community'
        db_table = 'community of Tolstoy lovers'


class Post(models.Model):
    """Model for records, field group is linked by model
    Group and author is linked by User."""
    text = models.TextField('article')
    pub_date = models.DateTimeField('year of writing', auto_now_add=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        verbose_name='group name',
        related_name='community',
        blank=True,
        null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
        related_name='author_posts')

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'notes of famous people'
        db_table = 'all post'
