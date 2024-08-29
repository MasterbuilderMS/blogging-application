from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from django.contrib.auth.models import User
from django.urls import reverse


def home(request):
    context = {
        "posts": Post.objects.all()
    }
    return render(request, "blog/home.html", context=context)


class PostListView(ListView):
    paginate_by = 5
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]


class UserPostListView(ListView):
    paginate_by = 5
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["content", "date_posted"]

    def form_valid(self, form):
        form.instance.post = Post.objects.get(pk=self.kwargs.get("pk"))
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={"pk": self.object.post.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self) -> bool:
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self) -> bool:
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html", context={"title": "about"})


def search_feature(request):
    # Check if the request is a post request.
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']

        # Filter your model by the search query

        posts = Post.objects.filter(content__contains=search_query)
        return render(request, 'blog/searched.html', {'query': search_query, 'posts': posts})
    else:
        return render(request, 'blog/searched.html', {})
