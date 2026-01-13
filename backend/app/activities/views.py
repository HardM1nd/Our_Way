from rest_framework import viewsets, permissions, status from rest_framework.decorators import action from rest_framework.response import Response from django.shortcuts import get_object_or_404 from .models import ActivityCategory, Activity, ActivityLog, ActivityReward, ActivityTimer from .serializers import ( ActivityCategorySerializer, ActivitySerializer, ActivityLogSerializer, ActivityRewardSerializer, ActivityTimerSerializer ) from .services import ActivityService from app.api.permissions import IsOwnerOrReadOnly
class ActivityCategoryViewSet(viewsets.ModelViewSet): queryset = ActivityCategory.objects.all() serializer_class = ActivityCategorySerializer permission_classes = [permissions.IsAuthenticatedOrReadOnly]
class ActivityViewSet(viewsets.ModelViewSet): queryset = Activity.objects.all() serializer_class = ActivitySerializer permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

@action(detail=True, methods=['post'])
def mark_complete(self, request, pk=None):
    activity = self.get_object()
    # create a log and mark it completed
    data = {'activity': activity.id}
    serializer = ActivityLogSerializer(data=data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    log = serializer.save()
    ActivityService.complete_activity(log, award_points=True)
    return Response(ActivityLogSerializer(log).data)
class ActivityLogViewSet(viewsets.ModelViewSet): queryset = ActivityLog.objects.all() serializer_class = ActivityLogSerializer permission_classes = [permissions.IsAuthenticated]
def get_queryset(self):
    qs = super().get_queryset()
    # users can only see their logs unless staff
    if not self.request.user.is_staff:
        qs = qs.filter(user=self.request.user)
    return qs

@action(detail=True, methods=['post'])
def complete(self, request, pk=None):
    log = self.get_object()
    ActivityService.complete_activity(log, award_points=True)
    return Response(ActivityLogSerializer(log).data)
class ActivityRewardViewSet(viewsets.ModelViewSet): queryset = ActivityReward.objects.all() serializer_class = ActivityRewardSerializer permission_classes = [permissions.IsAuthenticated]
@action(detail=True, methods=['post'])
def claim(self, request, pk=None):
    reward = self.get_object()
    if reward.claimed:
        return Response({'detail': 'Already claimed'}, status=status.HTTP_400_BAD_REQUEST)
    ActivityService.claim_reward(reward, request.user)
    return Response(ActivityRewardSerializer(reward).data)
class ActivityTimerViewSet(viewsets.ModelViewSet): queryset = ActivityTimer.objects.all() serializer_class = ActivityTimerSerializer permission_classes = [permissions.IsAuthenticated]
def get_queryset(self):
    if self.request.user.is_staff:
        return super().get_queryset()
    return self.queryset.filter(user=self.request.user)

@action(detail=True, methods=['post'])
def stop(self, request, pk=None):
    timer = self.get_object()
    timer.stop()
    # potentially grant xp based on duration
    ActivityService.process_timer(timer)
    return Response(ActivityTimerSerializer(timer).data)

@action(detail=False, methods=['post'])
def start(self, request):
    # start a new timer for a given activity (activity id in payload optional)
    activity_id = request.data.get('activity')
    activity = None
    if activity_id:
        activity = get_object_or_404(Activity, pk=activity_id)
    timer = ActivityTimer.objects.create(user=request.user, activity=activity)
    return Response(ActivityTimerSerializer(timer).data, status=status.HTTP_201_CREATED)
________________________________________
