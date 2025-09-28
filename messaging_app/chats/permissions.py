from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API
    - Only participants in a conversation can send, view, update, or delete messages
    """

    def has_object_permission(self, request, view, obj):
        # Must be logged in
        if not request.user or not request.user.is_authenticated:
            return False

        # Check if the user is part of the conversation
        participants = getattr(obj, "participants", None)
        conversation = getattr(obj, "conversation", None)

        if participants:
            is_participant = request.user in participants.all()
        elif conversation:
            is_participant = request.user in conversation.participants.all()
        else:
            is_participant = False

        if not is_participant:
            return False

        # Explicitly allow SAFE_METHODS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Explicitly check write methods: POST, PUT, PATCH, DELETE
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return True

        return False
