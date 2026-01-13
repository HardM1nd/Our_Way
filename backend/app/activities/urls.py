from django.urls import path, include from rest_framework.routers import DefaultRouter from .views import ( ActivityCategoryViewSet, ActivityViewSet, ActivityLogViewSet, ActivityRewardViewSet, ActivityTimerViewSet )
router = DefaultRouter() router.register(r'categories', ActivityCategoryViewSet, basename='activity-category') router.register(r'activities', ActivityViewSet, basename='activity') router.register(r'logs', ActivityLogViewSet, basename='activity-log') router.register(r'rewards', ActivityRewardViewSet, basename='activity-reward') router.register(r'timers', ActivityTimerViewSet, basename='activity-timer')
urlpatterns = [ path('', include(router.urls)), ]
________________________________________
