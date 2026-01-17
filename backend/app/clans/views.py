from rest_framework import viewsets, permissions 
from .models import Clan, ClanMember, ClanQuest 
from .serializers import ClanSerializer, ClanMemberSerializer, ClanQuestSerializer
class ClanViewSet(viewsets.ModelViewSet): 
    queryset = Clan.objects.all() 
    serializer_class = ClanSerializer 
    permission_classes = [permissions.IsAuthenticated]
def perform_create(self, serializer):
    serializer.save(created_by=self.request.user)
class ClanMemberViewSet(viewsets.ModelViewSet): 
    queryset = ClanMember.objects.all() 
    serializer_class = ClanMemberSerializer 
    permission_classes = [permissions.IsAuthenticated]
class ClanQuestViewSet(viewsets.ModelViewSet): 
    queryset = ClanQuest.objects.all() 
    serializer_class = ClanQuestSerializer 
    permission_classes = [permissions.IsAuthenticated]

from rest_framework.decorators import action
from rest_framework.response import Response

class ClanQuestViewSet(viewsets.ModelViewSet):
    queryset = ClanQuest.objects.all()
    serializer_class = ClanQuestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # показываем квесты кланов, где пользователь состоит
        clan_ids = user.clan_memberships.values_list('clan_id', flat=True)
        return self.queryset.filter(clan_id__in=clan_ids)

    @action(detail=True, methods=['post'])
    def contribute(self, request, pk=None):
        quest = self.get_object()
        contribution = int(request.data.get('contribution', 1))
        quest.total_progress = (quest.total_progress or 0) + contribution
        if quest.total_progress >= quest.required_progress:
            quest.completed = True
        quest.save()
        return Response(ClanQuestSerializer(quest).data)
