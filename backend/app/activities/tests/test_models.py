from django.test import TestCase from django.contrib.auth import get_user_model from app.activities.models import ActivityCategory, Activity, ActivityLog
User = get_user_model()
class ModelsTestCase(TestCase): def setUp(self): self.user = User.objects.create_user(username='tester', password='pass') self.cat = ActivityCategory.objects.create(name='Productivity') self.activity = Activity.objects.create(title='Read book', owner=self.user, category=self.cat, points=15)
def test_activity_creation(self):
    self.assertEqual(self.activity.title, 'Read book')
    self.assertEqual(self.activity.points, 15)

def test_activity_log_mark_complete(self):
    log = ActivityLog.objects.create(activity=self.activity, user=self.user)
    log.mark_completed()
    self.assertEqual(log.status, 'completed')
    self.assertTrue(log.points_awarded >= 0)
    self.assertIsNotNone(log.completed_at)
________________________________________
app/activities/tests/test_views.py
app/activities/tests/test_views.py
from django.urls import reverse from rest_framework.test import APITestCase from django.contrib.auth import get_user_model from app.activities.models import ActivityCategory, Activity
User = get_user_model()
class ActivitiesViewTests(APITestCase): def setUp(self): self.user = User.objects.create_user(username='apiuser', password='pass') self.client.login(username='apiuser', password='pass') self.cat = ActivityCategory.objects.create(name='Health')
def test_create_activity(self):
    url = reverse('activity-list')
    data = {'title': 'Morning run', 'category': self.cat.id, 'points': 20}
    resp = self.client.post(url, data, format='json')
    self.assertEqual(resp.status_code, 201)
    self.assertEqual(resp.data['title'], 'Morning run')

def test_start_stop_timer(self):
    # create activity
    act = Activity.objects.create(title='Focus session', owner=self.user, category=self.cat)
    start_url = reverse('activity-timer-list') + 'start/'
    resp = self.client.post(start_url, {'activity': act.id}, format='json')
    self.assertIn(resp.status_code, (200, 201))
    timer_id = resp.data['id']
    stop_url = reverse('activity-timer-detail', args=[timer_id]) + 'stop/'
    resp2 = self.client.post(stop_url, format='json')
    self.assertEqual(resp2.status_code, 200)
________________________________________
app/activities/fixtures/sample_activities.json
[ { "model": "activities.activitycategory", "pk": 1, "fields": { "name": "Health", "slug": "health", "description": "Physical and mental health tasks" } }, { "model": "activities.activity", "pk": 1, "fields": { "title": "Morning Jog", "description": "Run 30 minutes", "owner": 1, "category": 1, "points": 20, "difficulty": 1, "active": true } } ]
________________________________________
