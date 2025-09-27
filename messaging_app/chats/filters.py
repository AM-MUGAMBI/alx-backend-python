import django_filters
from django.db.models import Q
from .models import Message, User

class MessageFilter(django_filters.FilterSet):
    # Filter messages where the conversation includes a participant by user_id
    participant = django_filters.NumberFilter(method='filter_by_participant')

    # Filter messages sent after this datetime (inclusive)
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')

    # Filter messages sent before this datetime (inclusive)
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['participant', 'sent_after', 'sent_before']

    def filter_by_participant(self, queryset, name, value):
        # Return messages whose conversation participants include user with id=value
        return queryset.filter(conversation__participants__user_id=value)

