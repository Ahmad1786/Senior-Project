from django.db import models
from django.conf import settings

class Server(models.Model):
    group_name = models.CharField(max_length=30)
    group_icon = models.BinaryField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)

    # These string methods are giving a lot of error : should keep simple for now
    def __str__(self):
        # return "Group: " + self.group_name + ", created on " + self.date_created
        return f"{self.group_name} [Server ID {self.id}]"
    
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
        # return "User: " + self.self.user.name + ", joined " + self.server.group_name + " on " + self.date_joined
        return f"Participation {self.id}"
    
    # override save method to default display_name to user's first + last name
    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = f"{self.user.first_name} {self.user.last_name}"
        super().save(*args, **kwargs)



