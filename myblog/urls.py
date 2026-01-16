from django.urls import path

from myblog.views import PostListView, PostDetailView, PostCreateView, ContactView, PostUpdateView, PostDeleteView

app_name = 'myblog'

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/create/", PostCreateView.as_view(), name='post_create'),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name='post_update'),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name='post_delete'),
    path("contacts/", ContactView.as_view(), name="contacts"),
]