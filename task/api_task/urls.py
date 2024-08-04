from django.urls import path
from .views import CreateMemberView, DeleteMemberView, RegisterView, LoginView, TaskView,CommentView, Allmemeber

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('members/', CreateMemberView.as_view(), name='create-member'),
    path('members/<int:pk>/', DeleteMemberView.as_view(), name='delete-member'),
    path('tasks/', TaskView.as_view(), name='task-list-create'),
    path('tasks/<int:id>/', TaskView.as_view(), name='task-list-create'),
    path('comment/', CommentView.as_view(), name='comment-list'),
    path('comment/<int:id>/', CommentView.as_view(), name='comment_one'),
    path('allmember/<str:email>/', Allmemeber.as_view(), name='allmember'),
    # path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    # path('tasks/<int:pk>/members/', TaskMemberView.as_view(), name='task-member'),
    # path('tasks/<int:pk>/members/list/', TaskMembersListView.as_view(), name='task-member-list'),
    # path('tasks/<int:task_id>/comments/', CommentListView.as_view(), name='comment-list'),
    # path('tasks/<int:task_id>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    # path('tasks/<int:pk>/status/', UpdateTaskStatusView.as_view(), name='task-status-update'),
]
