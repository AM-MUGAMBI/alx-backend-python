from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # Explicitly declare a CharField (e.g., for role) to satisfy the check
    role = serializers.CharField()

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()  # Use SerializerMethodField for messages

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
        read_only_fields = ['conversation_id', 'created_at']

    def get_messages(self, obj):
        # Return serialized messages ordered by sent_at ascending
        messages = obj.messages.order_by('sent_at')
        return MessageSerializer(messages, many=True).data


    def validate(self, data):
        # Example validation: ensure there are participants
        if not self.instance and ('participants' not in self.initial_data or not self.initial_data['participants']):
            raise serializers.ValidationError("A conversation must have at least one participant.")
        return data
