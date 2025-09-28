import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    """
    Filter messages by participant user ID and sent_at datetime range.
    """

    # Filter messages where the conversation includes a participant by user_id
    participant = django_filters.NumberFilter(method='filter_by_participant')

    # Filter messages sent after this datetime (inclusive)
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')

    # Filter messages sent before this datetime (inclusive)
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['participant', 'sent_after', 'sent_before']

    def filter_by_participant(self, queryset, _, value):
        """
        Filter queryset to messages whose conversation participants include user with given user_id.
        """
        return queryset.filter(conversation__participants__user_id=value)
