from django.db import models from django.conf import settings from django.utils.text import slugify
User = settings.AUTH_USER_MODEL
class ActivityCategory(models.Model): name = models.CharField(max_length=100, unique=True) slug = models.SlugField(max_length=120, unique=True, blank=True) description = models.TextField(blank=True)
class Meta:
    verbose_name = 'Activity Category'
    verbose_name_plural = 'Activity Categories'

def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.name)
    super().save(*args, **kwargs)

def __str__(self):
    return self.name
class Activity(models.Model): title = models.CharField(max_length=200) description = models.TextField(blank=True) owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities') category = models.ForeignKey(ActivityCategory, on_delete=models.SET_NULL, null=True, related_name='activities') points = models.PositiveIntegerField(default=10) difficulty = models.PositiveSmallIntegerField(default=1) active = models.BooleanField(default=True) created_at = models.DateTimeField(auto_now_add=True) due_date = models.DateTimeField(null=True, blank=True)
class Meta:
    ordering = ['-created_at']

def __str__(self):
    return self.title
class ActivityLog(models.Model): STATUS_CHOICES = ( ('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ) activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='logs') user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs') notes = models.TextField(blank=True) points_awarded = models.IntegerField(default=0) status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') created_at = models.DateTimeField(auto_now_add=True) completed_at = models.DateTimeField(null=True, blank=True)
class Meta:
    ordering = ['-created_at']

def mark_completed(self, award_points=True, timestamp=None):
    from django.utils import timezone
    if self.status == 'completed':
        return
    self.status = 'completed'
    self.completed_at = timestamp or timezone.now()
    if award_points:
        self.points_awarded = self.activity.points
    self.save()

def __str__(self):
    return f'{self.user} -> {self.activity} [{self.status}]'
class ActivityReward(models.Model): REWARD_TYPES = ( ('points', 'Points'), ('achievement', 'Achievement'), ('xp', 'Experience'), ) activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='rewards') type = models.CharField(max_length=30, choices=REWARD_TYPES) value = models.CharField(max_length=255, help_text='Value depends on type. For points/xp store integer, for achievement store achievement id or slug.') claimed = models.BooleanField(default=False) created_at = models.DateTimeField(auto_now_add=True)
def __str__(self):
    return f'{self.activity.title} -> {self.type}:{self.value}'
class ActivityTimer(models.Model): user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_timers') activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='timers', null=True, blank=True) started_at = models.DateTimeField(auto_now_add=True) stopped_at = models.DateTimeField(null=True, blank=True) active = models.BooleanField(default=True) duration_seconds = models.PositiveIntegerField(default=0)
def stop(self, timestamp=None):
    from django.utils import timezone
    if not self.active:
        return
    self.stopped_at = timestamp or timezone.now()
    self.duration_seconds = int((self.stopped_at - self.started_at).total_seconds())
    self.active = False
    self.save()

def __str__(self):
    return f'Timer {self.id} by {self.user} ({\"active\" if self.active else \"stopped\"})'
