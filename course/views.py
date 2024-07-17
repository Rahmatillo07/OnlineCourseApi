from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from .models import Course, Topic, Video, Comment, LikeDislike, User
from .serializers import CourseSerializer, TopicSerializer, VideoSerializer, CommentSerializer, LikeDislikeSerializer, \
    RegisterSerializer, MessageSerializer
from .permissions import AdminRequiredPermission, AuthorPermission, ManagerPermission

from rest_framework.viewsets import ModelViewSet


class RegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get(self, request):
        return Response({'message': "Ro'yxatdan o'tish uchun ma'lumotlaringizni kiriting!"})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        new_user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        new_user.set_password(validated_data['password'])
        new_user.save()

        return redirect('rest_framework:login')


class CourseApiView(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AdminRequiredPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']


class TopicApiView(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [ManagerPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class VideoApiView(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [ManagerPermission]


class CommentApiView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AuthorPermission]


class LikeDislikeApiView(ModelViewSet):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer
    permission_classes = [AuthorPermission]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        old_like = LikeDislike.objects.filter(user=request.user, post=data['post']).first()
        if old_like:
            if old_like.like == data['like']:
                old_like.delete()
            else:
                old_like.like = data['like']
                old_like.save()
                return Response(serializer.data)
        else:
            self.perform_create(serializer)
            return Response(serializer.data)


def send_message_to_email(t, m):
    users = User.objects.all()
    receivers = [user.email for user in users if user.email]

    if receivers:
        send_mail(t, m, settings.EMAIL_HOST_USER, receivers)


class EmailMessageApiView(APIView):

    def get(self, request):
        return Response({'message': 'Barcha foydalanuvchilar emailiga xabar yuborish!!!'})

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()
            send_message_to_email(message.title, message.text)
            return Response(serializer.data)
        return Response(serializer.errors)
