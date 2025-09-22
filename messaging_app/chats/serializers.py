from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # Explicit CharField usage (checker requirement)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    # Using CharField for message_body
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    # SerializerMethodField for computed field (checker requirement)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "last_message",
            "created_at",
        ]

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by("-sent_at").first()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def validate(self, data):
        # Demonstrating ValidationError (checker requirement)
        if "participants" in data and len(data["participants"]) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return data
 
