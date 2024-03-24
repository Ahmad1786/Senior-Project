from django.db import models
from django.conf import settings

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



