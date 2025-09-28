from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    - Allow only authenticated users (global REST_FRAMEWORK default ensures this)
    - Allow only participants of a conversation to view/send/update/delete messages or access that conversation.
    """

    def has_permission(self, request, view):
        # Must be authenticated (global setting enforces this), keep explicit check
        if not request.user or not request.user.is_authenticated:
            return False

        # For list/create views, allow -- object permissions will be enforced later.
        # For creating a conversation, any authenticated user is allowed.
        return True

    def has_object_permission(self, request, view, obj):
        """
        obj may be a Conversation or Message instance.
        - If Conversation: user must be in participants.
        - If Message: user must be in message.conversation.participants.
        """
        user = request.user

        if isinstance(obj, Conversation):
            return obj.participants.filter(pk=user.pk).exists()

        if isinstance(obj, Message):
            conv = obj.conversation
            return conv.participants.filter(pk=user.pk).exists()

        # default deny
        return False
