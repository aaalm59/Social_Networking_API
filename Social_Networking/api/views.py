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
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_signup(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User successfully registered'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([permissions.AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    # print('username', username, '------', 'password', password)
    user = authenticate(request, username=username, password=password)
    # print('---------', user)

    if user:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        response_data = {
            'access': access_token,
            'refresh': refresh_token,
            # 'user': UserSerializer(user).data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_users(request):     
        keyword = request.query_params.get('q', '')
        users = User.objects.filter(
            Q(email__iexact=keyword) | Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword)
        ).exclude(id=request.user.id)[:10]
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_friend_request(request, receiver_id):
        try:
            receiver = User.objects.get(pk=receiver_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if receiver == request.user:
            return Response({"detail": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        existing_request = FriendRequest.objects.filter(sender=request.user, receiver=receiver)
        if existing_request.exists():
            return Response({"detail": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)

        # Creating the friend request without using a serializer
        friend_request = FriendRequest.objects.create(sender=request.user, receiver=receiver, status='pending')

        return Response({"detail": "Friend request sent successfully."}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_friend_request(request, request_id):
    print("accepted-----------------------------",request_id)
    friend_request = FriendRequest.objects.filter(pk=request_id, status='pending').first() #receiver=request.user,
    print('friend_request',friend_request)
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
    pending_requests = FriendRequest.objects.filter(status='pending') #receiver=request.user,
    print('pending_requests',pending_requests)
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
