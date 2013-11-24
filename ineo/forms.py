# coding=utf-8
from django import forms
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from ineo.models import Comment


class CommentAddForm(forms.ModelForm):
    captcha = CaptchaField(label=u'Капча')

    class Meta:
        model = Comment
        exclude = ['cdate', 'status', 'parent', 'ip']

    def __init__(self, *args, **kwargs):
        super(CommentAddForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs = {'rows': 5}

        self.helper = FormHelper()
        self.helper.form_id = 'id_comment_form'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        # self.helper.form_action = ''
        self.helper.add_input(Submit('submit', u'Отправить'))

        self.fields['content_type'].widget = forms.HiddenInput()
        self.fields['object_id'].widget = forms.HiddenInput()


class CommentReplyForm(forms.ModelForm):
    captcha = CaptchaField(label=u'Капча')

    class Meta:
        model = Comment
        exclude = ['cdate', 'status', 'ip']

    def __init__(self, *args, **kwargs):
        super(CommentReplyForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs = {'rows': 5}

        self.helper = FormHelper()
        self.helper.form_id = 'id_comment_form'
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        # self.helper.form_action = ''
        self.helper.add_input(Submit('submit', u'Отправить'))

        self.fields['content_type'].widget = forms.HiddenInput()
        self.fields['object_id'].widget = forms.HiddenInput()
        self.fields['parent'].widget = forms.HiddenInput()
