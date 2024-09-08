from django.urls import path
from apps.tasks.views.tag_views import *
from apps.tasks.views.task_views import *
urlpatterns = [
    path('tasks/', TaskViewListCreateGenericView.as_view(), name='task-list'),
    path('tags/', TagListAPIView.as_view(), name='tag-list'),
    path('tags/create/', TagCreateAPIView.as_view(), name='tag-create'),
    path('tags/<int:pk>/', TagDetailAPIView.as_view(), name='tag-detail'),
    path('tags/<int:pk>/update/', TagUpdateAPIView.as_view(), name='tag-update'),
]