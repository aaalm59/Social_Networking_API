from django.urls import path
from .views import SearchUsersAPIView, FriendRequestAPIView, AcceptFriendRequestAPIView, \
    RejectFriendRequestAPIView, ListFriendsAPIView, ListPendingRequestsAPIView, FriendRequestRateLimitAPIView, \
    CustomAuthToken, SignupAPIView

urlpatterns = [
    path('search-users/', SearchUsersAPIView.as_view(), name='search-users'),
    path('friend-request/', FriendRequestAPIView.as_view(), name='friend-request'),
    path('accept-friend-request/<int:pk>/', AcceptFriendRequestAPIView.as_view(), name='accept-friend-request'),
    path('reject-friend-request/<int:pk>/', RejectFriendRequestAPIView.as_view(), name='reject-friend-request'),
    path('list-friends/', ListFriendsAPIView.as_view(), name='list-friends'),
    path('list-pending-requests/', ListPendingRequestsAPIView.as_view(), name='list-pending-requests'),
    path('friend-request-rate-limit/', FriendRequestRateLimitAPIView.as_view(), name='friend-request-rate-limit'),
    path('login/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
]

