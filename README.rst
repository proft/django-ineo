===========
django-ineo
===========

Простая система комментариев для любой модели. Есть возможность ответа на комментарий вплоть до второго уровня :).
Модуль зависит от `django-crispy-forms <https://github.com/maraujop/django-crispy-forms/>` и `django-simple-captcha <https://github.com/mbi/django-simple-captcha>`.


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

3. Добавляем в целевую модель поле comments с ссылкой на GenericRelation (models.py) и указываем ссылку на страницу с добавлением комментариев для этой модели в `get_comment_add_url`. Пример:

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
            return reverse('comment_add', kwargs={'pk': self.pk})

4. Добавляем в views.py два вида для добавления комментариев и ответов на комментарии

::

    from django.views.generic.edit import FormView
    from django.core.urlresolvers import reverse
    from django.shortcuts import get_object_or_404
    from django.contrib.contenttypes.models import ContentType
    from django.http import HttpResponseRedirect
    from django.contrib import messages
    from ineo.forms import CommentAddForm, CommentReplyForm


    class AnimalCommentAddView(FormView):
        template_name = 'ineo/comment_add.html'
        form_class = CommentAddForm

        def get_initial(self):
            obj = get_object_or_404(Animal, pk=self.kwargs['pk'])
            self.obj = obj
            ctype = ContentType.objects.get_for_model(obj)
            init = {'content_type': ctype, 'object_id': obj.id}
            return init

        def form_valid(self, form):
            form.save()
            messages.info(self.request, u'Спасибо, Ваш комментарий добавлен!')
            return HttpResponseRedirect(self.get_success_url())

        def get_success_url(self):
            return reverse('animal', kwargs={'pk': self.obj.id})


    class AnimalCommentReplyView(FormView):
        template_name = 'ineo/comment_add.html'
        form_class = CommentReplyForm

        def get_initial(self):
            self.obj = get_object_or_404(Animal, pk=self.kwargs['pk'])
            parent = self.kwargs['ppk']
            ctype = ContentType.objects.get_for_model(self.obj)
            init = {'content_type': ctype, 'object_id': self.obj.id, 'parent': parent}
            return init

        def form_valid(self, form):
            form.save()
            messages.info(self.request, u'Спасибо, Ваш комментарий добавлен!')
            return HttpResponseRedirect(self.get_success_url())

        def get_success_url(self):
            return reverse('animal', kwargs={'pk': self.obj.id})


5. В шаблоне модели вставляем место для вывода списка комментариев

::

    {% extends "base.html" %}
    {% load ineo_tags %}

    {% block content %}
    {{ animal.title }}

    {% comment_list animal %}

    {% endblock content %}

4. Описываем адреса для добавления комментариев и ответов на комментарии в urls.py

::

    url(r'^animal/add/(?P<pk>[\d]+)/$', AnimalCommentAddView.as_view(), name='comment_add'),
    url(r'^animal/add/(?P<pk>[\d]+)/(?P<ppk>[\d]+)/$', AnimalCommentReplyView.as_view(), name='comment_reply'),
