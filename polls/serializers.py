from rest_framework import serializers
from .models import Poll, Choice, Vote

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_by', 'created_at', 'choices']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields =['id', 'poll', 'choice', 'voted_at']
        read_only_fields = ('voted_by',)