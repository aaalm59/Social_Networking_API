# api/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import UserProfile, FriendRequest
from .serializers import UserProfileSerializer, FriendRequestSerializer,UserSerializer, UserSignupSerializer
from django.db.models import Q
from django.utils import timezone
from .models import UserProfile, FriendRequest
from rest_framework import  permissions, status
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User successfully registered'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print('username',username,'------','password',password)

    user = authenticate(request, username=username, password=password)
    print('---------',user)
    
    if user:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_users(request):
    keyword = request.query_params.get('keyword', '')
    
    if '@' in keyword:
        user = User.objects.filter(email__iexact=keyword).first()
        if user:
            serializer = UserProfileSerializer(user.profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        users = User.objects.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword))
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({'message': 'Invalid search criteria'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_friend_request(request, receiver_id):
    if not request.user.is_authenticated:
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    sender_profile = request.user.profile
    receiver_profile = UserProfile.objects.get(pk=receiver_id)

    if sender_profile != receiver_profile:
        if not FriendRequest.objects.filter(sender=sender_profile.user, receiver=receiver_profile.user, status='pending').exists():
            if FriendRequest.objects.filter(Q(sender=receiver_profile.user, receiver=sender_profile.user, status='pending') | Q(sender=sender_profile.user, receiver=receiver_profile.user, status='accepted')).exists():
                return Response({'error': 'Friend request already exists or already friends'}, status=status.HTTP_400_BAD_REQUEST)

            if sender_profile.sent_requests.filter(created_at__gte=timezone.now() - timezone.timedelta(minutes=1)).count() >= 3:
                return Response({'error': 'You cannot send more than 3 friend requests within a minute'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            friend_request = FriendRequest.objects.create(sender=sender_profile.user, receiver=receiver_profile.user, status='pending')
            friend_request.save()

            return Response({'message': 'Friend request sent successfully'}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Invalid friend request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.filter(pk=request_id, receiver=request.user, status='pending').first()

    if friend_request:
        friend_request.status = 'accepted'
        friend_request.save()
        return Response({'message': 'Friend request accepted successfully'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid friend request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_friend_request(request, request_id):
    friend_request = FriendRequest.objects.filter(pk=request_id, receiver=request.user, status='pending').first()

    if friend_request:
        friend_request.status = 'rejected'
        friend_request.save()
        return Response({'message': 'Friend request rejected successfully'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid friend request'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def friends_list(request):
    friends = User.objects.filter(friend_requests_received__status='accepted',friend_requests_received__sender=request.user,).union(User.objects.filter(
        friend_requests_sent__status='accepted',
        friend_requests_sent__receiver=request.user,
    )
)

    serializer = UserProfileSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def pending_friend_requests(request):
    pending_requests = FriendRequest.objects.filter(receiver=request.user, status='pending')
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
