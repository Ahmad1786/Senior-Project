from django.db import models
from django.conf import settings
from django.utils import timezone
import secrets
import string
from datetime import timedelta

class Server(models.Model):
    group_name = models.CharField(max_length=30)
    group_icon = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Participation', related_name='servers')

    def __str__(self):
        return f"{self.group_name}"
    
class Participation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participations")
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="participations")
    display_name = models.CharField(max_length=30, null=False, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    points = models.IntegerField(default=0)
    is_owner = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'server')

    def __str__(self):
        return f"[{self.user}] -> [{self.server}] {'(Owner)' if self.is_owner else ''}"
    
    def server_name(self):
        return self.server.group_name
    
    # override save method to default display_name to user's first + last name
    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = f"{self.user.first_name} {self.user.last_name}"
        super().save(*args, **kwargs)

class Invitation(models.Model):
    token = models.CharField(max_length=7, unique=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    invited_email = models.EmailField(blank=True, null=True)
    invited_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    expiration_time = models.DateTimeField()

    @classmethod
    def create_invitation(cls, server, invited_email=None):
        expiration_time = timezone.now() + timedelta(hours=24)  # Invitation expires in 24 hours
        token = cls.generate_token()
        return cls.objects.create(token=token, server=server, invited_email=invited_email, expiration_time=expiration_time)

    @staticmethod
    def generate_token():
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(7))


