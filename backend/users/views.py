from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import User
from .serializers import (
    UserSerializer, UserCreateSerializer, LoginSerializer, ChangePasswordSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    User ViewSet: Provides CRUD operations for users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        """Return different serializers based on action"""
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        """Return different permissions based on action"""
        if self.action in ['login', 'register']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        User login endpoint
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Generate or get Token
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        User logout endpoint
        """
        if request.user.is_authenticated:
            request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'})

    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        User registration endpoint
        """
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create Token
        token = Token.objects.create(user=user)

        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current user info
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Change password endpoint
        """
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()

        # Regenerate Token
        request.user.auth_token.delete()
        token = Token.objects.create(user=request.user)

        return Response({
            'message': 'Password changed successfully',
            'token': token.key
        })

    @action(detail=False, methods=['get'])
    def students(self, request):
        """
        Get all students list
        """
        students = User.objects.filter(role='student')
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def teachers(self, request):
        """
        Get all teachers list
        """
        teachers = User.objects.filter(role='teacher')
        serializer = UserSerializer(teachers, many=True)
        return Response(serializer.data)
