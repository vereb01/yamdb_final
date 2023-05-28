from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import (IsAdmin, IsAdminModeratorOwnerOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommetSerializer,
                          GenreSerializer, RegisterDataSerializer,
                          ReviewSerializer, TitleSerializer, TokenSerializer,
                          UserEditSerializer, UserSerializer,
                          WatchTitleSerializer)


class SignUpView(APIView):
    def post(self, request):
        serializer = RegisterDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')

        try:
            user, _ = User.objects.get_or_create(
                username=username,
                email=email
            )
        except IntegrityError as error:
            raise ValidationError(
                ('Ошибка при попытке создать новую запись '
                 f'в базе с username={username}, email={email}')
            ) from error

        user.save()
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='YaMDb registration',
            message=f'Your confirmation code: {confirmation_code}',
            from_email=None,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )

        if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
        ):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=[
            'get',
            'patch',
        ],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewSet(CreateModelMixin, ListModelMixin,
                      DestroyModelMixin, viewsets.GenericViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CreateModelMixin, ListModelMixin,
                   DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleSerializer
        return WatchTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorOwnerOrReadOnly]

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorOwnerOrReadOnly
    ]

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title)
        return Comment.objects.filter(review=review)
