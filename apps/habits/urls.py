from django.urls import path

from apps.habits.views import HabitCreateAPIView, HabitRetrieveUpdateDestroyView, HabitPublicListAPIView

app_name = 'habits'

urlpatterns = [
    path('create/', HabitCreateAPIView.as_view(), name='habit-create'),
    path('<int:pk>/', HabitRetrieveUpdateDestroyView.as_view(), name='habit-retrieve-update-destroy'),
    path('public/', HabitPublicListAPIView.as_view(), name='public-list')

]
