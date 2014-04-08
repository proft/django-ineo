# -*- coding: utf-8 -*-
from django import template
from ineo.models import Comment

register = template.Library()


@register.inclusion_tag('ineo/comment_list.html')
def comment_list(obj):
    comments = obj.comments.filter(parent__isnull=True).exclude(status=Comment.STATUS_HIDDEN) if hasattr(obj, 'comments') else None
    url_comment_add = obj.get_comment_add_url() if hasattr(obj, 'get_comment_add_url') else None
    return {'comments': comments, 'url_comment_add': url_comment_add}
