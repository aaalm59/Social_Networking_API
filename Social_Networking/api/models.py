# from django.contrib.auth.models import User
# from django.db import models

# class FriendRequest(models.Model):
#     sender = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
#     receiver = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
#     status = models.CharField(choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add any additional user profile fields if needed


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional fields as needed for your user profile


class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender} to {self.receiver} ({self.status})"
