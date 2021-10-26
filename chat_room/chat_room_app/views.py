"""Views for the chat app."""

from django.contrib.auth import get_user_model
from django.http.response import HttpResponseRedirect, HttpResponse
import requests
from .models import (
    ChatSession, ChatSessionMember, ChatSessionMessage, deserialize_user
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer

from notifications.utils import notify
from notifications import default_settings as notifs_settings

from django.shortcuts import render, resolve_url, redirect


class ChatSessionView(APIView):
    """Manage Chat sessions."""

    #permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """create a new chat session."""
        user = request.user

        chat_session = ChatSession.objects.create(owner=user)

        return Response({
            'status': 'SUCCESS', 'uri': chat_session.uri,
            'message': 'New chat session created'
        })

    def patch(self, request, *args, **kwargs):
        """Add a user to a chat session."""
        User = get_user_model()

        uri = kwargs['uri']
        username = request.data['username']
        user = User.objects.get(username=username)

        chat_session = ChatSession.objects.get(uri=uri)
        owner = chat_session.owner

        if owner != user:  # Only allow non owners join the room             
            chat_session.members.get_or_create(
                user=user, chat_session=chat_session
            )

        owner = deserialize_user(owner)
        members = [
            deserialize_user(chat_session.user) 
            for chat_session in chat_session.members.all()
        ]
        members.insert(0, owner)  # Make the owner the first member
        return Response ({
            'status': 'SUCCESS', 'members': members,
            'message': '%s joined the chat' % user.username,
            'user': deserialize_user(user)
        })
    

class ChatSessionMessageView(APIView):
    """Create/Get Chat session messages."""
    renderer_classes = [TemplateHTMLRenderer]

    #permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """return all messages in a chat session."""
        uri = kwargs['uri']
        print(request.META)
        chat_session = ChatSession.objects.get(uri=uri)
        messages = [chat_session_message.to_json() 
            for chat_session_message in chat_session.messages.all()]
        template = "template.html"

        return Response({
            'id': chat_session.id, 'uri': chat_session.uri,
            'messages': messages
        }, template_name=template)

    def post(self, request, *args, **kwargs):
        """create a new message in a chat session."""
        uri = kwargs['uri']
        message = request.data['message']

        user = request.user
        chat_session = ChatSession.objects.get(uri=uri)

        chat_session_message = ChatSessionMessage.objects.create(
            user=user, chat_session=chat_session, message=message
        )
        #TODO MAKE SURE OF THIS
        notif_args = {
            'source': user,
            'source_display_name': user.get_full_name(),
            'category': 'chat', 'action': 'Sent',
            'obj': chat_session_message.id,
            'short_description': 'You have a new message', 
            'silent': True,
            'extra_data': {
                notifs_settings.NOTIFICATIONS_WEBSOCKET_URL_PARAM:
                chat_session.uri,
                'message': chat_session_message.to_json()
            }
        }
        notify(**notif_args, channels=['websocket'])

        return Response({
            'status': 'SUCCESS', 'uri': chat_session.uri, 'message': message,
            'user': deserialize_user(user)
        })

def chat_room_list(request):
    print(request.session.get("access_token",0))
    chat_list = ChatSession.objects.all()
    context = {'chat_room_list':chat_list}
    return render(request, "chatroomlist.html", context)

def handle_create_new_chatroom(request):
    print(request.session.get("access_token", 0))
    token = "Token " + request.session.get("access_token", 0)
    print(token)
    url = "http://localhost:8000/chat_room/chats/"
    header = {"Authorization": token}
    req = requests.post(url,headers=header).json()
    print(req)
    uri = req.get("uri", 0)
    response = HttpResponseRedirect(url + str(uri) + "/messages/")
    return response

def join_chat(request):
    #TODO
    pass

def send_message(request):
    #TODO
    pass

def del_all_chat_room(request):
    ChatSession.objects.all().delete()
    return HttpResponse
