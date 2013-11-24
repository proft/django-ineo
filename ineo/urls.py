from django.conf.urls import patterns, url

from ineo.views import CommentListView, CommentAddView

urlpatterns = patterns(
    '',
    # url(r'^$', CommentListView.as_view(), name="list"),
    url(r'^add/$', CommentAddView.as_view(), name="add"),
    url(r'^add/(?P<pk>[\d]+)/$', CommentAddView.as_view(), name="add_answer"),
)
