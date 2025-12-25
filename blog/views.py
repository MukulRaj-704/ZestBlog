from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Blog
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import CommentForm


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 5
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Blog.objects.filter(is_published=True).select_related('author')

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )

        return queryset



class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author')
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = self.object
            comment.author = request.user
            comment.save()

        return redirect('blog_detail', slug=self.object.slug)


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'slug', 'content', 'cover_image', 'is_published']
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'slug', 'content', 'cover_image', 'is_published']
    template_name = 'blog/blog_form.html'

    def test_func(self):
        blog = self.get_object()
        return blog.author == self.request.user


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')

    def test_func(self):
        blog = self.get_object()
        return blog.author == self.request.user


@login_required
def toggle_like(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)

    return redirect('blog_detail', slug=slug)
