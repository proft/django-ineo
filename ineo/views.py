# -*- coding: utf-8 -*-

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
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
        form.save()
        messages.info(self.request, u'Спасибо, Ваш комментарий добавлен!')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('comments:list')
