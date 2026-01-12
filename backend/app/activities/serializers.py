from rest_framework import serializers from .models import ActivityCategory, Activity, ActivityLog, ActivityReward, ActivityTimer from django.utils import timezone
class ActivityCategorySerializer(serializers.ModelSerializer): class Meta: model = ActivityCategory fields = ['id', 'name', 'slug', 'description']
class ActivitySerializer(serializers.ModelSerializer): owner = serializers.PrimaryKeyRelatedField(read_only=True) category = serializers.PrimaryKeyRelatedField(queryset=ActivityCategory.objects.all(), required=False, allow_null=True)
class Meta:
    model = Activity
    fields = ['id', 'title', 'description', 'owner', 'category', 'points', 'difficulty', 'active', 'created_at', 'due_date']
class ActivityLogSerializer(serializers.ModelSerializer): user = serializers.PrimaryKeyRelatedField(read_only=True) activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all())
class Meta:
    model = ActivityLog
    fields = ['id', 'activity', 'user', 'notes', 'points_awarded', 'status', 'created_at', 'completed_at']
    read_only_fields = ['points_awarded', 'status', 'created_at', 'completed_at']

def create(self, validated_data):
    request = self.context.get('request')
    validated_data['user'] = request.user
    log = super().create(validated_data)
    return log
class ActivityRewardSerializer(serializers.ModelSerializer): activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all())
class Meta:
    model = ActivityReward
    fields = ['id', 'activity', 'type', 'value', 'claimed', 'created_at']
    read_only_fields = ['claimed', 'created_at']
class ActivityTimerSerializer(serializers.ModelSerializer): user = serializers.PrimaryKeyRelatedField(read_only=True) activity = serializers.PrimaryKeyRelatedField(queryset=Activity.objects.all(), required=False, allow_null=True)
class Meta:
    model = ActivityTimer
    fields = ['id', 'user', 'activity', 'started_at', 'stopped_at', 'active', 'duration_seconds']
    read_only_fields = ['started_at', 'stopped_at', 'active', 'duration_seconds']

def create(self, validated_data):
    request = self.context.get('request')
    validated_data['user'] = request.user
    timer = super().create(validated_data)
    return timer
