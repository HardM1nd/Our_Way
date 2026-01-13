from django.dispatch import Signal
Sent when an activity log is completed: providing_args: ['activity_log']
activity_completed = Signal() # payload: activity_log (ActivityLog instance)
Sent when a reward is claimed: payload reward, user
reward_claimed = Signal()
________________________________________
