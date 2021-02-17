from django.urls import path

from .views import ItemSelectView, UserProfileListView, ItemCreateView, ItemUpdateView, ItemDeleteView, \
    CommentCreateView, CommentSelectView, CommentDeleteView, ban_user, unban_user, answer_comment

urlpatterns = [
    path('all-news/', ItemSelectView.as_view()),
    path('create-item/', ItemCreateView.as_view()),
    path('update-item/<int:pk>', ItemUpdateView.as_view()),
    path('delete-item/<int:pk>', ItemDeleteView.as_view()),
    path('create-comment/', CommentCreateView.as_view()),
    path('item-comments/', CommentSelectView.as_view()),
    path('delete-comment/<int:pk>', CommentDeleteView.as_view()),
    path('get-profiles/', UserProfileListView.as_view(), name="all-profiles"),
    path('ban-user/', ban_user),
    path('unban-user/', unban_user),
    path('answer-comment/', answer_comment),
]