from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task, Comment, Member
from .serializers import TaskSerializer,  CommentSerializer, UserSerializer, TaskaddSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .serializers import MemberSerializer
from rest_framework.exceptions import NotFound

# Authentication Views
# User Register view


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save()
            return Response({"Message": "Your email " + request.data.get('email') + " ID is successfully registerd"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login view


class LoginView(APIView):
    def post(self, request):
        if not request.data.get('email') or not request.data.get('password'):
            return Response({"error": "email & password required !!"}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
                "access": access_token,
                "refresh": refresh_token
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# Create Member
class CreateMemberView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Memeber delete


class DeleteMemberView(generics.DestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            member = self.request.user.member_set.get(pk=self.kwargs['pk'])
            return member
        except Member.DoesNotExist:
            # Raise a NotFound exception if the Member object is not found
            raise NotFound(detail="Member not found")

# CReate Task


class TaskView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None, format=None):
        
        if id:
            task_get = Task.objects.get(id=id)
            serializer = TaskSerializer(task_get)
        else:
            task_get = Task.objects.all()
            serializer = TaskSerializer(task_get, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.data['member']:
            return Response({"error": "Member Id requied"}, status=status.HTTP_400_BAD_REQUEST)
        request_data = request.data.copy()
        request_data['member'] = request.data['member']
        print(request_data)
        serializer = TaskaddSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'post_data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id, format=None):
        
        task = get_object_or_404(Task, id=id)
        request_data = request.data.copy()
        data = {
            'title': request_data.get('title', task.title),
            'description': request_data.get('description', task.description),
            'due_date': request_data.get('due_date', task.due_date),
            'status': request_data.get('status', task.status),
        }
        serializer = TaskaddSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'post_data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        task = get_object_or_404(Task, id=id)
        task.delete()
        return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class CommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None, format=None):

        if id:
            Comment_get = Comment.objects.get(id=id)
            serializer = CommentSerializer(Comment_get)
        else:
            Comment_get = Comment.objects.all()
            serializer = CommentSerializer(Comment_get, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'post_data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        comment = get_object_or_404(Comment, id=id)
        request_data = request.data.copy()
        data = {
            'task': request_data.get('task', comment.task),
            'user': request_data.get('user', comment.user),
            'content': request_data.get('content', comment.content)
            
        }
        serializer = CommentSerializer(comment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'post_data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        return Response({'message': 'comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class Allmemeber(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, email, format=None):


        if email:
            member_id = get_object_or_404(Member,email=email)
            Comment_get = list(Task.objects.filter(member=member_id).values_list('title','description','due_date','status'))
        return Response({'data': Comment_get}, status=status.HTTP_200_OK)
