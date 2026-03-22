from blog.models import Message

def unread_messages(request):
    if request.user.is_authenticated:
        try:
            count = Message.objects.filter(
                conversation__participants=request.user,
                is_read=False
            ).exclude(sender=request.user).count()
            return {'unread_message_count': count}
        except Exception:
            return {'unread_message_count': 0}
    return {'unread_message_count': 0}