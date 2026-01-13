from django.utils import timezone from .models import ActivityLog, ActivityReward, ActivityTimer from app.core.services import NotificationService from app.achivments.models import Achievement, UserAchievement from app.Focus.models import FocusExperience, FocusMemberProgress from app.Clans.models import ClanMember # for future clan-based rewards
class ActivityService: @staticmethod def complete_activity(activity_log: ActivityLog, award_points: bool = True): if activity_log.status == 'completed': return activity_log activity_log.mark_completed(award_points=award_points) # create rewards (if any) for reward in activity_log.activity.rewards.filter(claimed=False): # by default mark points-type rewards as auto-claimed if reward.type == 'points': try: pts = int(reward.value) except Exception: pts = activity_log.points_awarded or activity_log.activity.points # notify user / increment profile points (example) NotificationService.send(activity_log.user, f'You gained {pts} points for completing {activity_log.activity.title}') reward.claimed = True reward.save() elif reward.type == 'achievement': # try create UserAchievement (if exists) try: ach = Achievement.objects.get(pk=int(reward.value)) except Exception: ach = None if ach: UserAchievement.objects.get_or_create(user=activity_log.user, achievement=ach) reward.claimed = True reward.save() elif reward.type == 'xp': try: xp = int(reward.value) except Exception: xp = activity_log.points_awarded or activity_log.activity.points # simple xp addition: create FocusExperience record FocusExperience.objects.create(user=activity_log.user, points=xp, timestamp=timezone.now()) # adjust FocusMemberProgress if user is part of project's members (best-effort) # This logic is intentionally lightweight: projects/runs are separate. reward.claimed = True reward.save() # emit any signals in signals.py (import there) return activity_log
@staticmethod
def claim_reward(reward: ActivityReward, user):
    if reward.claimed:
        return reward
    if reward.type == 'points':
        # example: create ActivityLog to reflect points claimed
        # real impl should increase user's total points in profile model
        reward.claimed = True
        reward.save()
    elif reward.type == 'achievement':
        try:
            ach = Achievement.objects.get(pk=int(reward.value))
        except Exception:
            ach = None
        if ach:
            UserAchievement.objects.get_or_create(user=user, achievement=ach)
        reward.claimed = True
        reward.save()
    elif reward.type == 'xp':
        try:
            xp = int(reward.value)
        except Exception:
            xp = 0
        FocusExperience.objects.create(user=user, points=xp, timestamp=timezone.now())
        reward.claimed = True
        reward.save()
    NotificationService.send(user, f'Reward claimed: {reward.type}')
    return reward

@staticmethod
def process_timer(timer: ActivityTimer):
    # Award xp/points based on timer.duration_seconds and optionally activity.points/difficulty
    seconds = timer.duration_seconds or 0
    minutes = max(1, seconds // 60)
    xp = minutes * 1  # 1 xp per minute as example
    FocusExperience.objects.create(user=timer.user, points=xp, timestamp=timezone.now())
    NotificationService.send(timer.user, f'You earned {xp} XP for a {minutes}-minute session.')
    return xp
________________________________________
