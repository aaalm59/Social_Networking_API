from django.urls import path
from .views import user_signup,user_login,search_users,send_friend_request,accept_friend_request,reject_friend_request,friends_list,pending_friend_requests


urlpatterns = [
    path('signup/', user_signup, name='user_signup'),
    path('login/', user_login, name='user_login'),
    path('search/', search_users, name='search_users'),
    path('send-friend-request/<int:receiver_id>/', send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('reject-friend-request/<int:request_id>/', reject_friend_request, name='reject_friend_request'),
    path('friends-list/', friends_list, name='friends_list'),
    path('pending-friend-requests/', pending_friend_requests, name='pending_friend_requests'),
]
