from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter, ConversationFilter
from .pagination import MessagePagination

from django_filters.rest_framework import DjangoFilterBackend

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ConversationFilter
    search_fields = ["participants__first_name", "participants__last_name", "participants__email"]
    ordering_fields = ["created_at"]

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get("participants", [])
        if not isinstance(participant_ids, list) or len(participant_ids) < 2:
            return Response(
                {"detail": "participants must be a list of at least two user ids."},
                status=status.HTTP_400_BAD_REQUEST
            )

        users = User.objects.filter(user_id__in=participant_ids)
        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        conversation.save()
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        Restrict conversations to those the request.user participates in.
        """
        user = self.request.user
        if not user or not user.is_authenticated:
            return Conversation.objects.none()
        return Conversation.objects.filter(participants__pk=user.pk).distinct()

    @action(detail=True, methods=["post"])
    def add_message(self, request, pk=None):
        """
        Alternative endpoint to add message to conversation: /conversations/{pk}/add_message/
        Payload: { "message_body": "..." }
        Sender will be request.user
        """
        conversation = get_object_or_404(Conversation, pk=pk)
        # permission check: ensure requester is participant
        self.check_object_permissions(request, conversation)

        message_body = request.data.get("message_body")
        if not message_body:
            return Response({"detail": "message_body is required."}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related("sender", "conversation")
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ["message_body"]
    ordering_fields = ["sent_at"]

    def get_queryset(self):
        """
        Return only messages that belong to conversations the request.user participates in.
        Optionally filter by conversation via query params handled by MessageFilter.
        """
        user = self.request.user
        if not user or not user.is_authenticated:
            return Message.objects.none()

        # messages in conversations where user is participant
        qs = Message.objects.filter(conversation__participants__pk=user.pk).distinct()
        return qs

    def perform_create(self, serializer):
        """
        When creating a message, set sender to request.user and ensure the user is participant of conversation.
        Expect request.data to include 'conversation' (id) or creation via nested route.
        """
        conversation = serializer.validated_data.get("conversation")
        if not conversation:
            # attempt to get conversation id from request data
            conv_id = self.request.data.get("conversation_id") or self.request.data.get("conversation")
            if conv_id:
                conversation = get_object_or_404(Conversation, pk=conv_id)
            else:
                raise serializers.ValidationError("conversation or conversation_id is required.")

        # permission: user must be participant of conversation
        if not conversation.participants.filter(pk=self.request.user.pk).exists():
            from rest_framework import serializers as drf_serializers
            raise drf_serializers.ValidationError("You are not a participant of this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)
