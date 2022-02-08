from django.db import models

# Create your models here.
from account.models import CustomUser


class Problema(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(CustomUser,
                               on_delete=models.DO_NOTHING,
                               related_name='problemy')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)


class CodeImage(models.Model):
    image = models.ImageField(upload_to='problem_img')
    problema = models.ForeignKey(Problema,
                                 on_delete=models.CASCADE,
                                 related_name='images')


class Reply(models.Model):
    problema = models.ForeignKey(Problema,
                                 on_delete=models.CASCADE,
                                 related_name='replies')
    body = models.TextField()
    image = models.ImageField(upload_to='reply_img')
    author = models.ForeignKey(CustomUser,
                               on_delete=models.DO_NOTHING,
                               related_name='replies')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.body[:11]}...'


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(CustomUser,
                               on_delete=models.DO_NOTHING,
                               related_name='commenty')
    reply = models.ForeignKey(Reply,
                              on_delete=models.CASCADE,
                              related_name='commenty')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


