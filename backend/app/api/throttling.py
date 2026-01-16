from rest_framework.throttling import UserRateThrottle
class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'
class SustainedRateThrottle(UserRateThrottle): 
    scope = 'sustained'
#Add corresponding settings in REST_FRAMEWORK if you enable throttling:
REST_FRAMEWORK = {
'DEFAULT_THROTTLE_CLASSES': [
'app.api.throttling.BurstRateThrottle',
'app.api.throttling.SustainedRateThrottle',
],
'DEFAULT_THROTTLE_RATES': {
'burst': '60/min',
'sustained': '1000/day',
}
}

