from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Trade
from .serializers import TradeSerializer, RegisterSerializer, LoginSerializer, UserSerializer
from .permissions import IsOwner


class TradeViewSet(viewsets.ModelViewSet):
    serializer_class = TradeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Trade.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@parser_classes([JSONParser])
def register_view(request: Request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@parser_classes([JSONParser])
def login_view(request: Request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(
        request,
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password']
    )
    if user is None:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    login(request, user)
    return Response(UserSerializer(user).data)


@api_view(['POST'])
@parser_classes([JSONParser])
def logout_view(request: Request):
    logout(request)
    return Response({'detail': 'Logged out'})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@ensure_csrf_cookie
def me_view(request: Request):
    if not request.user.is_authenticated:
        return Response({ 'authenticated': False })
    return Response(UserSerializer(request.user).data)
