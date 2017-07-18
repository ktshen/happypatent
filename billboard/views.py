from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.db import transaction
from proposals.views import FileAttachmentViewMixin

from .models import Post, User, Comment
from .forms import PostModelForm, CommentModelForm


@transaction.non_atomic_requests
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        kwargs = super(PostDetailView, self).get_context_data(**kwargs)
        kwargs["comment_form"] = CommentModelForm
        kwargs["comments"] = Comment.objects.filter(post=self.object).order_by('-created')
        return kwargs


class PostCreateView(LoginRequiredMixin, FileAttachmentViewMixin, CreateView):
    model = Post
    template_name = "billboard/post_create.html"
    form_class = PostModelForm
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = User.objects.get(username=self.request.user.username)
        self.object.save()
        super(PostCreateView, self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class PostUpdateView(LoginRequiredMixin, FileAttachmentViewMixin, UpdateView):
    model = Post
    template_name = "billboard/post_update.html"
    form_class = PostModelForm
    slug_field = "slug"
    slug_url_kwarg = "slug"


@transaction.non_atomic_requests
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 5
    ordering = ['-update', '-created']


@login_required
def post_remove(request):
    if request.method == "POST":
        post_slug = request.POST["slug"]
        try:
            obj = Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            return HttpResponseBadRequest("Post Not Found.")
        if obj.author.username == request.user.username:
            title = obj.title
            obj.delete()
        else:
            return HttpResponseBadRequest("No privilege to do this action.")
        messages.add_message(request, messages.SUCCESS, 'You have successfully removed the post "%s".' % title)
        return HttpResponseRedirect(reverse("billboard:list"))


class CommentCreateView(LoginRequiredMixin, CreateView):
    http_method_names = [u'post']
    model = Comment
    fields = ["text"]

    def post(self, request, *args, **kwargs):
        self.post_slug = kwargs["slug"]
        return super(CommentCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = get_object_or_404(Post, slug=self.post_slug)
        self.object.created_by = get_object_or_404(User, username=self.request.user.username)
        self.object.save()
        return HttpResponseRedirect(reverse("billboard:detail", args=(self.post_slug,))+"#comment")


