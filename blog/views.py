from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count, Case, When, IntegerField, Value
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import Blog, Comment
from .forms import CommentForm, BlogForm
from accounts.models import UserProfile


User = get_user_model()


from django.db.models import Count

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 6

    def get_queryset(self):
        queryset = Blog.objects.filter(
            is_published=True
        ).select_related('author')

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )

        if self.request.user.is_authenticated:
            try:
                user_profile, _ = UserProfile.objects.get_or_create(
                    user=self.request.user
                )
                following_user_ids = user_profile.follows.values_list(
                    'user_id', flat=True
                )
                queryset = queryset.annotate(
                    is_followed=Case(
                        When(author_id__in=following_user_ids, then=Value(0)),
                        default=Value(1),
                        output_field=IntegerField()
                    )
                ).order_by('is_followed', '-created_at')
            except Exception:
                queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Following IDs for follow buttons
        if self.request.user.is_authenticated:
            try:
                user_profile, _ = UserProfile.objects.get_or_create(
                    user=self.request.user
                )
                context['following_ids'] = set(
                    user_profile.follows.values_list('user_id', flat=True)
                )

                # Suggested users — not following yet
                already_following = user_profile.follows.all()
                context['suggested_users'] = UserProfile.objects.exclude(
                    user=self.request.user
                ).exclude(
                    id__in=already_following
                ).annotate(
                    follower_count=Count('followed_by')
                ).order_by('-follower_count')[:4]

            except Exception:
                context['following_ids'] = set()
                context['suggested_users'] = []
        else:
            context['following_ids'] = set()
            context['suggested_users'] = []

        # Trending blogs — top liked
        context['trending_blogs'] = Blog.objects.filter(
            is_published=True
        ).annotate(
            total_likes=Count('likes')
        ).order_by('-total_likes')[:5]

        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author')
        context['comment_form'] = CommentForm()

        if self.request.user.is_authenticated:
            author_profile, _ = UserProfile.objects.get_or_create(
                user=self.object.author
            )
            user_profile, _ = UserProfile.objects.get_or_create(
                user=self.request.user
            )
            context['is_following_author'] = (
                author_profile in user_profile.follows.all()
            )
        else:
            context['is_following_author'] = False

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

@login_required
def following_feed(request):
    my_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    following_profiles = my_profile.follows.all()
    following_users = User.objects.filter(profile__in=following_profiles)
    blogs = Blog.objects.filter(
        author__in=following_users,
        is_published=True
    ).select_related('author').order_by('-created_at')

    return render(request, 'blog/following_feed.html', {'blogs': blogs})


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog_list')

    def test_func(self):
        return self.get_object().author == self.request.user


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')

    def test_func(self):
        return self.get_object().author == self.request.user


@login_required
def toggle_like(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        liked = False
    else:
        blog.likes.add(request.user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'count': blog.total_likes()
        })

    return redirect('blog_detail', slug=slug)
@login_required
def follow_toggle(request, username):
    if request.method != 'POST':
        # redirect to accounts profile URL
        return redirect('user_profile', username=username)

    target_user = get_object_or_404(User, username=username)

    if request.user == target_user:
        return redirect('user_profile', username=username)

    my_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    target_profile, _ = UserProfile.objects.get_or_create(user=target_user)

    if target_profile in my_profile.follows.all():
        my_profile.follows.remove(target_profile)
        is_following = False
    else:
        my_profile.follows.add(target_profile)
        is_following = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'is_following': is_following,
            'followers_count': target_profile.followers_count,
        })

    return redirect('user_profile', username=username)


from .models import Blog, Comment, Conversation, Message
from django.db.models import Max


@login_required
def inbox(request, conversation_id=None):
    conversations = request.user.conversations.annotate(
        last_message_time=Max('messages__created_at')
    ).order_by('-last_message_time')

    # Add other_participant to each conversation
    for convo in conversations:
        convo.other_user = convo.other_participant(request.user)

    active_conversation = None
    messages_qs = None
    other_user = None

    if conversation_id:
        active_conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            participants=request.user
        )
        active_conversation.messages.exclude(
            sender=request.user
        ).update(is_read=True)

        messages_qs = active_conversation.messages.select_related(
            'sender', 'shared_blog'
        ).order_by('created_at')

        other_user = active_conversation.other_participant(request.user)

    return render(request, 'blog/inbox.html', {
        'conversations': conversations,
        'active_conversation': active_conversation,
        'messages': messages_qs,
        'other_user': other_user,
    })

@login_required
def start_conversation(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return redirect('inbox')

    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=target_user
    ).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, target_user)

    return redirect('conversation_detail', conversation_id=conversation.id)


@login_required
@login_required
def delete_message(request, message_id):
    # Any participant can delete any message in their conversation
    message = get_object_or_404(
        Message,
        id=message_id,
        conversation__participants=request.user
    )

    if request.method == 'POST':
        message.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message_id': message_id})
        return redirect('conversation_detail', conversation_id=message.conversation.id)

    return JsonResponse({'success': False})


@login_required
def share_blog(request, slug):
    if request.method != 'POST':
        return redirect('blog_detail', slug=slug)

    blog = get_object_or_404(Blog, slug=slug)
    friend_username = request.POST.get('username', '').strip()

    if not friend_username:
        return redirect('blog_detail', slug=slug)

    friend = get_object_or_404(User, username=friend_username)

    # Get or create conversation
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=friend
    ).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, friend)

    # Send blog as message
    Message.objects.create(
        conversation=conversation,
        sender=request.user,
        body=f"Check out this blog: {blog.title}",
        shared_blog=blog
    )

    return redirect('conversation_detail', conversation_id=conversation.id)


@login_required
def get_mutual_friends(request):
    """Returns users who follow each other — for share suggestions"""
    my_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Mutual friends = people I follow AND who follow me back
    following = set(my_profile.follows.values_list('user_id', flat=True))
    followers = set(my_profile.followed_by.values_list('user_id', flat=True))
    mutual_ids = following & followers

    mutual_friends = User.objects.filter(id__in=mutual_ids).values(
        'id', 'username'
    )

    return JsonResponse({'friends': list(mutual_friends)})


@login_required
@login_required
def send_file(request, conversation_id):
    if request.method != 'POST':
        return redirect('conversation_detail', conversation_id=conversation_id)

    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        participants=request.user
    )

    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return JsonResponse({'success': False, 'error': 'No file'})

    file_name = uploaded_file.name
    extension = file_name.split('.')[-1].lower()
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    file_type = 'image' if extension in image_extensions else 'document'

    message = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        body='',
        file=uploaded_file,
        file_name=file_name,
        file_type=file_type
    )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'file_url': message.file.url,  # Cloudinary returns full URL
            'file_name': message.file_name,
            'file_type': message.file_type,
            'sender': request.user.username,
            'sender_id': request.user.id,
            'timestamp': message.created_at.strftime('%H:%M'),
        })

    return redirect('conversation_detail', conversation_id=conversation_id)