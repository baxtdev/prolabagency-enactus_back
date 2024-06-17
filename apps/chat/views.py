from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from rest_framework.authtoken.models import Token

from apps.chat.models import ChatRoom
# Create your views here.
@login_required(login_url='/admin/')
def rooms(request):
    user = request.user
    rooms =[chat for chat in ChatRoom.objects.all() if user.chat_info in chat.users.all()]
    print(rooms)
    rooms = ChatRoom.objects.all()
    return render(request,'index.html',{'rooms':rooms})

@login_required(login_url='/admin/')
def start_chat(request, uuid):
    chat_room: ChatRoom = get_object_or_404(ChatRoom, uuid=uuid)
    if request.user not in [i.user for i in chat_room.users.all()]:
        messages.warning(request, 'Вы не являетесь участником чата.')
        return redirect('/admin/')
    
    to_user = chat_room.users.exclude(user=request.user).first()
    print(to_user)
    token = Token.objects.get_or_create(user=request.user)[0]
    return render(request, 'chat.html',
                  {'chat_room': chat_room, 'messages': chat_room.messages.all()[::-1], 'to_user': to_user,
                   'token': str(token)})