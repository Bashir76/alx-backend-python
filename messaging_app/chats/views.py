from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expects a list of participant user_ids.
        """
        participant_ids = request.data.get("participants", [])
        if len(participant_ids) < 2:
            return Response(
                {"error": "A conversation must have at least two participants."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        users = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(users)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages in conversations.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Expects: sender_id, conversation_id, message_body
        """
        sender_id = request.data.get("sender_id")
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")

        if not sender_id or not conversation_id or not message_body:
            return Response(
                {"error": "sender_id, conversation_id, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        sender = get_object_or_404(User, user_id=sender_id)
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body,
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

