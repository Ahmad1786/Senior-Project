from django.db import models
from django.conf import settings
from django.utils import timezone
import secrets
import string
from datetime import timedelta
from django.core.mail import send_mail
from django.http import JsonResponse
from users.models import User



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
        # Check for existing invitation expiring within the next 12 hours
        existing_invitation = cls.objects.filter(
            server=server,
            expiration_time__lte=timezone.now() + timedelta(hours=12),
            invited_email=invited_email
        ).first()

        if existing_invitation:
            return existing_invitation

        expiration_time = timezone.now() + timedelta(hours=24)  # Invitation expires in 24 hours
        token = cls.generate_token()
        return cls.objects.create(token=token, server=server, invited_email=invited_email, expiration_time=expiration_time)

    @staticmethod
    def generate_token():
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(7))

    @classmethod
    def send_invitation_emails(cls, server, emails):
        valid_emails = []
        invalid_emails = []

        for email in emails:
            if Participation.objects.filter(server=server, user__email=email).exists():
                invalid_emails.append(email)
            else:
                valid_emails.append(email)

        invitations_sent = []

        for email in valid_emails:
            user = User.objects.filter(email=email).first()
            invited_user = user if user else None

            invitation = cls.create_invitation(server, invited_email=email)
            invitation.invited_user = invited_user
            invitation.save()

            invitations_sent.append(email)

            send_mail(
                'Invitation to Cohabitat',
                f'Hey, you have been invited to join {server.group_name}. Sign in to or create an account with Cohabitat and use the invitation code shown below to join the group.\nInvitation Code: {invitation.token}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

        if invalid_emails:
            return JsonResponse({'message': 'Unable to send invite email to the following emails:', 'invalid_emails': invalid_emails})
        elif invitations_sent:
            return JsonResponse({'message': 'Successfully sent invite email to the following emails:', 'valid_emails': invitations_sent})
        else:
            return JsonResponse({'message': 'No valid emails provided.'})

