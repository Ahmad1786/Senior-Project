import json
from django.contrib.auth import get_user_model
from posts.models import Chore, Event, Bill, Comment
from servers.models import Server, Participation
from datetime import timedelta
from django.utils import timezone
import random
from django.contrib.auth.hashers import make_password

# going to skip the deleting of all objects for now

User = get_user_model()

# Create a Superuser / admin
super_username = 'admin'
super_password = 'admin'
if not User.objects.filter(username=super_username).exists():
    User.objects.create_superuser(password=super_password, username=super_username, first_name='CoHabitat', last_name='Admin')
    print('Superuser created username: admin, password: admin')
else:
    print('Superuser already exists with username admin already exists')

# for each keep the same password for all
PASSWORD = 'adminadmin' # admin password will be just admin (in main script)
hashed_password = make_password(PASSWORD)

# create the remaining objects
# 7 types of objects in order: 0User, 1Server, 2Participation, 3Chore/Task, 4Event, 5Bill, 6Comment

# read in json data
with open('manual_data.json') as f:
    data = json.load(f) # array of len 7

Users, Servers, Participations, Chores, Events, Bills, Comments = data

for u in Users:
    user = User.objects.create(password=hashed_password, first_name=u['first_name'], last_name=u['last_name'], email=u['email'])
    user.save()

for s in Servers:
    server = Server.objects.create(group_name=s['name'])
    server.save()

for p in Participations:
    participation = Participation.objects.create(user=User.objects.get(first_name=p['user']), server=Server.objects.get(group_name=p['house']), is_owner=p['is_owner'])
    participation.save()

for t in Chores:
    chore = Chore.objects.create(server=Server.objects.get(group_name=t['house']), 
            creator=User.objects.get(first_name=t['creator']), 
            post_name=t['name'], description=t['description'], due_date=timezone.now() + timedelta(days=10))
    chore.save()

for e in Events:
    event = Event.objects.create(server=Server.objects.get(group_name=e['house']), 
            creator=User.objects.get(first_name=e['creator']), 
            post_name=e['name'], description=e['description'], date_time=timezone.now() + timedelta(days=random.randint(5, 30)))
    event.save()

for b in Bills:
    bill = Bill.objects.create(server=Server.objects.get(group_name=b['house']), 
            creator=User.objects.get(first_name=b['creator']), 
            post_name=b['name'], description=b['description'], cost=b['cost'])
    bill.save()

for c in Comments:

    try:
        chore = Chore.objects.get(post_name=c['post_name'])
        post=chore
    except Chore.DoesNotExist:
        pass
    try:
        event = Event.objects.get(post_name=c['post_name'])
        post=event
    except Event.DoesNotExist:
        pass
    try:
        bill = Bill.objects.get(post_name=c['post_name'])
        post=bill
    except Bill.DoesNotExist:
        pass
    
    comment = Comment.objects.create(author=User.objects.get(first_name=c['author']), content=c['text'])
    if post == chore:
        comment.task = chore
    elif post == event:
        comment.event = event
    elif post == bill:
        comment.bill = bill
    comment.save()