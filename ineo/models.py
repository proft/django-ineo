# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse


MAX_COMMENT_LENGTH = 2000


class CommentManager(models.Manager):
    def visible(self):
        return super(CommentManager, self).get_query_set().filter(status=Comment.STATUS_PUBLIC)


class Comment(models.Model):
    STATUS_HIDDEN, STATUS_PUBLIC, STATUS_NEW = range(3)
    STATUS_CHOICES = (
        (STATUS_HIDDEN, u'Скрыт'),
        (STATUS_PUBLIC, u'Виден'),
        (STATUS_NEW, u'Новый'),
    )

    name = models.CharField(u'Имя', max_length=100)
    email = models.EmailField(u'E-Mail', blank=True)
    comment = models.TextField(u'Отзыв')
    cdate = models.DateTimeField(u'Дата добавления', auto_now_add=True)
    status = models.PositiveSmallIntegerField(u'Статус', choices=STATUS_CHOICES, default=STATUS_NEW)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', verbose_name=u'Родительский комментарий')
    ip = models.GenericIPAddressField('IP', unpack_ipv4=True, blank=True, null=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    objects = CommentManager()

    class Meta:
        verbose_name_plural = u'Комментарии'
        verbose_name = u'комментарий'
        ordering = ['-cdate']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.comment = self.comment[:MAX_COMMENT_LENGTH]
        super(Comment, self).save(*args, **kwargs)

    def has_descendant(self):
        return bool(self.children.count())

    def is_descendant(self):
        return True if self.parent else False

    def get_reply_url(self):
        url, kwargs = self.content_object.prepare_comment_reply_url()
        kwargs['pk'] = self.pk
        return reverse(url, kwargs=kwargs)
