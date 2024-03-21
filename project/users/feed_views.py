from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import Bill, Chore, Event, Comment
from servers.models import Server, Participation
from django.http import HttpResponse
from django.db.models import F, Q
from django.db import models

@login_required
def feed_view(request):
    # Get the servers the current user is in
    servers = Server.objects.filter(participations__user=request.user)

    # Get the last login time of the user
    #last_login = request.user.last_login

    # Filter posts and comments for the servers the user is in since their last login time
    events = Event.objects.filter(server__in=servers)#, date_created__gte=last_login)
    bills = Bill.objects.filter(server__in=servers)#, date_created__gte=last_login)
    chores = Chore.objects.filter(server__in=servers)#, date_created__gte=last_login)
    # Filter comments for the posts (tasks, events, bills) that belong to servers the user is in
    comments = Comment.objects.filter(
        models.Q(task__server__in=servers) |
        models.Q(event__server__in=servers) |
        models.Q(bill__server__in=servers),
        #date_time__gte=last_login
    )

    # Construct dictionaries for each post/comment with necessary information
    feed_items = []

    for event in events:
        feed_items.append({
            'heading': f"{event.creator} created an event: {event.post_name}",
            'description': event.description,
            'date': event.date_created
        })

    for bill in bills:
        feed_items.append({
            'heading': f"{bill.creator} created a bill: {bill.post_name}",
            'description': bill.description,
            'date': bill.date_created
        })

    for chore in chores:
        feed_items.append({
            'heading': f"{chore.creator} created a chore: {chore.post_name}",
            'description': chore.description,
            'date': chore.date_created
        })

    for comment in comments:
        post_type = ""
        if comment.task:
            post_type = "chore"
        elif comment.event:
            post_type = "event"
        elif comment.bill:
            post_type = "bill"
        
        feed_items.append({
            'heading': f"{comment.author} commented on {post_type}",
            'description': comment.content,
            'date': comment.date_time
        })

    # Sort the feed items by date
    feed_items.sort(key=lambda x: x['date'], reverse=True)
    # print(feed_items)
    # Render the feed template with the feed items as context
    return render(request, 'feed.html', {'feed_items': feed_items, 'servers': servers})