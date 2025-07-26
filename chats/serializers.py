from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Handles user data serialization for API responses.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'phone_number', 'is_online', 'created_at']
        read_only_fields = ['id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    Includes sender information and handles message creation.
    """
    sender = UserSerializer(read_only=True)
    sender_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_id', 'conversation', 'content', 
                 'timestamp', 'is_read']
        read_only_fields = ['id', 'timestamp']

    def create(self, validated_data):
        """
        Create a new message.
        Automatically set sender from request user if not provided.
        """
        request = self.context.get('request')
        if request and not validated_data.get('sender_id'):
            validated_data['sender'] = request.user
        elif validated_data.get('sender_id'):
            validated_data['sender'] = User.objects.get(id=validated_data.pop('sender_id'))
        
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model.
    Handles nested relationships and includes recent messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    last_message = MessageSerializer(read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'participant_ids', 'messages', 
                 'last_message', 'message_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        """Return the total number of messages in this conversation"""
        return obj.messages.count()

    def create(self, validated_data):
        """
        Create a new conversation.
        Add participants from participant_ids and include request user.
        """
        participant_ids = validated_data.pop('participant_ids', [])
        request = self.context.get('request')
        
        conversation = Conversation.objects.create()
        
        # Add participants
        if participant_ids:
            participants = User.objects.filter(id__in=participant_ids)
            conversation.participants.set(participants)
        
        # Always include the request user as a participant
        if request and request.user:
            conversation.participants.add(request.user)
        
        return conversation

    def to_representation(self, instance):
        """
        Customize the representation to limit messages returned.
        Only return the most recent 50 messages to avoid large payloads.
        """
        representation = super().to_representation(instance)
        
        # Limit messages to most recent 50 for performance
        recent_messages = instance.messages.all()[:50]
        representation['messages'] = MessageSerializer(recent_messages, many=True).data
        
        return representation


class ConversationListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for conversation lists.
    Only includes essential information without all messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    last_message = MessageSerializer(read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'last_message', 'message_count', 
                 'created_at', 'updated_at']

    def get_message_count(self, obj):
        """Return the total number of messages in this conversation"""
        return obj.messages.count()
