import django_filters
from .models import Message, Conversation
from django.db.models import Q

class MessageFilter(django_filters.FilterSet):
    sender_id = django_filters.UUIDFilter(field_name="sender__user_id")
    conversation_id = django_filters.UUIDFilter(field_name="conversation__conversation_id")
    sent_after = django_filters.IsoDateTimeFilter(field_name="sent_at", lookup_expr="gte")
    sent_before = django_filters.IsoDateTimeFilter(field_name="sent_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["sender_id", "conversation_id", "sent_after", "sent_before"]


class ConversationFilter(django_filters.FilterSet):
    participant_id = django_filters.UUIDFilter(method="filter_by_participant")

    class Meta:
        model = Conversation
        fields = ["participant_id"]

    def filter_by_participant(self, queryset, name, value):
        return queryset.filter(participants__user_id=value).distinct()
