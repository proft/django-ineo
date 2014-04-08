# -*- coding: utf-8 -*-

from collections import defaultdict
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from ineo.models import Comment
from ineo.forms import CommentAddForm, CommentReplyForm


class CommentListView(ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'ineo/comment_list.html'


class CommentAddView(CreateView):
    form_class = CommentAddForm
    model = Comment
    template_name = 'ineo/comment_add.html'

    def form_valid(self, form):
        comment = form.save()

        if hasattr(settings, 'EMAIL_RECIPIENTS'):
            sender = settings.EMAIL_FROM
            subject = u"%s новый отзыв для %s" % (settings.EMAIL_SUBJECT_PREFIX, comment.content_object)
            message = u"Имя: %s\nEMail: %s\n\n%s\n\nУправление комментарием" % (comment.name,
                comment.email, comment.comment, reverse('admin:ineo_comment_change', args=[comment.id]))
            send_mail(subject, message, sender, settings.EMAIL_RECIPIENTS)

        messages.info(self.request, u'Спасибо, Ваш комментарий добавлен!')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('comments:list')


class IneoAddView(FormView):
    model = None
    url_kwargs = {}
    template_name = 'ineo/comment_add.html'
    form_class = CommentAddForm

    def get_initial(self):
        _url_kwargs = defaultdict(str)
        for k, v in self.url_kwargs.items():
            _url_kwargs[k] = self.kwargs[v]

        obj = get_object_or_404(self.model, **_url_kwargs)
        self.obj = obj
        ctype = ContentType.objects.get_for_model(obj)
        init = {'content_type': ctype, 'object_id': obj.id}
        return init

    def form_valid(self, form):
        comment = form.save()

        if hasattr(settings, 'EMAIL_RECIPIENTS'):
            edit_url = "http://%s%s" % (Site.objects.get_current(), reverse('admin:ineo_comment_change', args=[comment.id]))
            sender = settings.EMAIL_FROM
            subject = u"%s новый отзыв для %s" % (settings.EMAIL_SUBJECT_PREFIX, comment.content_object)
            message = u"Объект: %s\nИмя: %s\nEMail: %s\n\n%s\n\nУправление комментарием: %s" % (comment.content_object, comment.name, comment.email, comment.comment, edit_url)
            send_mail(subject, message.encode('utf-8'), sender, settings.EMAIL_RECIPIENTS)

        messages.info(self.request, u'Спасибо, Ваш комментарий добавлен!')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.obj.get_absolute_url()


class IneoReplyView(FormView):
    model = None
    url_kwargs = {'slug': 'slug'}
    template_name = 'ineo/comment_add.html'
    form_class = CommentReplyForm

    def get_initial(self):
        _url_kwargs = defaultdict(str)
        for k, v in self.url_kwargs.items():
            _url_kwargs[k] = self.kwargs[v]

        self.obj = get_object_or_404(self.model, **_url_kwargs)
        parent = self.kwargs['pk']
        ctype = ContentType.objects.get_for_model(self.obj)
        init = {'content_type': ctype, 'object_id': self.obj.id, 'parent': parent}
        return init

    def form_valid(self, form):
        comment = form.save()

        if hasattr(settings, 'EMAIL_RECIPIENTS'):
            edit_url = "http://%s%s" % (Site.objects.get_current(), reverse('admin:ineo_comment_change', args=[comment.id]))
            sender = settings.EMAIL_FROM
            subject = u"%s новый отзыв для %s" % (settings.EMAIL_SUBJECT_PREFIX, comment.content_object)
            message = u"Объект: %s\nИмя: %s\nEMail: %s\n\n%s\n\nУправление комментарием: %s" % (comment.content_object,
                comment.name, comment.email, comment.comment, edit_url)
            send_mail(subject, message.encode('utf-8'), sender, settings.EMAIL_RECIPIENTS)

        messages.info(self.request, u'Спасибо, Ваш комментарий добавлен!')
        self.url_kwargs = {}
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.obj.get_absolute_url()

