# -*- coding: utf-8 -*-

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail import send_mail

from ineo.models import Comment
from ineo.forms import CommentAddForm


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
