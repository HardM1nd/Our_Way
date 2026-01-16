from django.urls import path, include
urlpatterns = [ path('focus/', include('app.Focus.urls')), path('clans/', include('app.Clans.urls')), path('achivments/', include('app.achivments.api.py' if False else 'app.achivments.api')), # пример, можно заменить на конкретный путь # дополнительные пути вашего проекта ]
