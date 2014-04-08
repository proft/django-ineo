===========
django-ineo
===========

Простая система комментариев для любой модели. Есть возможность ответа на комментарий вплоть до второго уровня :).
Модуль зависит от [django-crispy-forms](https://github.com/maraujop/django-crispy-forms/) и [django-simple-captcha](https://github.com/mbi/django-simple-captcha).


Установка
=========

1. Установка модуля и зависимостей `pip install 'git+https://github.com/proft/django-ineo.git'`;
2. Добавляем `ineo` и зависимости в INSTALLED_APPS

::

    INSTALLED_APPS = (
        ...
        'ineo',
        'captcha',
        'crispy_forms',
    )

3. Добавляем в целевую модель поле comments с ссылкой на GenericRelation (models.py) и указываем ссылку на страницу с добавлением комментариев для этой модели в `get_comment_add_url`, в `prepare_comment_reply_url` указываем адрес для формы с ответом. Пример:

::

    from django.db import models
    from django.contrib.contenttypes import generic
    from django.core.urlresolvers import reverse
    from ineo.models import Comment


    class Animal(models.Model):
        title = models.CharField("Title", max_length=50)
        comments = generic.GenericRelation(Comment)

        class Meta:
            verbose_name = 'Animal'
            verbose_name_plural = 'Animals'

        def __unicode__(self):
            return self.title

        def get_comment_add_url(self):
            return reverse('animals:comment_add', kwargs={'pk': self.pk})

3. Описываем адреса для добавления комментариев и ответов на комментарии в urls.py

::
    
    from django.conf.urls import patterns, url
    from animals.models import Animal
    from ineo.views import IneoAddView, IneoReplyView

    urlpatterns = patterns('',
        url(r'^animal/(?P<slug>[-\w]+)/comment/add/$', IneoAddView.as_view(model=Animal, 
            url_kwargs={'slug': 'slug'}), name='comment_add'),
        url(r'^animal/(?P<slug>[-\w]+)/comment/add/(?P<pk>[\d]+)/$', IneoReplyView.as_view(model=Animal, 
            url_kwargs={'slug': 'slug'}), name='comment_reply'),            
    )
            

4. В шаблоне модели вставляем место для вывода списка комментариев

::

    {% extends "base.html" %}
    {% load ineo_tags %}

    {% block content %}
    {{ animal.title }}

    {% comment_list animal %}

    {% endblock content %}


