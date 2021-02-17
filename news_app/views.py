from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item, User, Comment
from .permissions import IsBunned
from .serializers import ItemSerializer, UserSerializer, CommentSerializer, ItemForViewSerializer, \
    CommentForViewSerializer
from rest_framework import generics, status


class UserProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serialized_users = UserSerializer(users, many=True)
        return Response({'users': serialized_users.data})


class ItemSelectView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serialized_items = ItemForViewSerializer(items, many=True)
        return Response({"items": serialized_items.data})


class ItemCreateView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAdminUser]


class ItemDeleteView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAdminUser]


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsBunned]

    def perform_create(self, serializer):
        try:
            item = Item.objects.get(pk=self.request.data['item_id'])
            serializer.save(user=self.request.user, item=item)
        except MultiValueDictKeyError:
            raise Http404


class CommentSelectView(APIView):
    def get(self, request):
        item = Item.objects.get(pk=request.data['item_id'])
        comments = Comment.objects.filter(item=item)
        serialized_items = CommentForViewSerializer(comments, many=True)
        return Response({"comments": serialized_items.data})


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]


@api_view(['POST'])
@permission_classes([IsAdminUser])
def ban_user(request):
    user_id = request.data['user_id']
    user = User.objects.get(pk=user_id)
    user.is_banned = True
    user.save()
    email = user.email
    send_mail(
        'Вы забанены на Новостном портале!',
        'Вы больше не можете оставлять комментарии.',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    message = 'user ' + email + ' is banned'
    return Response({'message': message})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def unban_user(request):
    user_id = request.data['user_id']
    user = User.objects.get(pk=user_id)
    user.is_banned = False
    user.save()
    message = 'user ' + user.email + ' is unbanned'
    return Response({'message': message})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def answer_comment(request):
    try:
        item = request.data['item_id']
        body = request.data['body']
        parent_comment = Comment.objects.get(pk=request.data['parent_id'])
        comment = Comment.objects.create(
            user=request.user,
            item=Item.objects.get(pk=item),
            body=body,
            parent=parent_comment
            )
        comment.save()

        answer_user = parent_comment.objects.user
        email = answer_user.email
        send_mail(
            'Ответ на ваш комментарий',
            'На ваш комментарий ответил другой пользователь.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return Response({'message': 'comment is created'}, status=status.HTTP_201_CREATED)
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

