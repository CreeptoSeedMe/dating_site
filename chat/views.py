from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from users.models import Profile

@login_required
def conversations(request):
    conversations = Conversation.objects.filter(
        Q(match__user1=request.user.profile) | Q(match__user2=request.user.profile)
    ).order_by('-last_message_at')
    return render(request, 'chat/conversations.html', {'conversations': conversations})

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.user.profile not in [conversation.match.user1, conversation.match.user2]:
        return redirect('conversations')

    messages = conversation.get_messages()
    return render(request, 'chat/conversation_detail.html', {'conversation': conversation, 'messages': messages})