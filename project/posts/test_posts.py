from django.shortcuts import render
from .models import Bill, Chore, Event, Comment
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404

# Sorry. About to completely violate the DRY principle :/

# note should have @login_required decorator but its okay for testing
def test_bill(request, id):
    
    bill = get_object_or_404(Bill, id=id)
    if bill is None:
        return HttpResponseNotFound("Bill not found")
    
    bill_fields = {}
    for field in Bill._meta.get_fields():
        field_value = getattr(bill, field.name, None)
        bill_fields[field.name] = field_value

    context = {
        "bill": bill,
        "bill_fields": bill_fields
    }

    return render(request, "posts/test-bill.html", context=context)

def test_chore(request, id):
    chore = get_object_or_404(Chore, id=id)
    if chore is None:
        return HttpResponseNotFound("Chore not found")
    
    chore_fields = {}
    for field in Chore._meta.get_fields():
        field_value = getattr(chore, field.name, None)
        chore_fields[field.name] = field_value

    context = {
        "chore": chore,
        "chore_fields": chore_fields
    }

    return render(request, "posts/test-chore.html", context=context)


def test_event(request, id):
    event = get_object_or_404(Event, id=id)
    if event is None:
        return HttpResponseNotFound("Event not found")
    
    event_fields = {}
    for field in Event._meta.get_fields():
        field_value = getattr(event, field.name, None)
        event_fields[field.name] = field_value

    context = {
        "event": event,
        "event_fields": event_fields
    }

    return render(request, "posts/test-event.html", context=context)


def test_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if comment is None:
        return HttpResponseNotFound("Comment not found")
    
    comment_fields = {}
    for field in Comment._meta.get_fields():
        field_value = getattr(comment, field.name, None)
        comment_fields[field.name] = field_value

    # get which post it belongs to (could be one of three)  
    post = comment.task or comment.event or comment.bill
    if comment.task:
        post_type = 'chore'
    elif comment.event:
        post_type = 'event'
    elif comment.bill:
        post_type = 'bill'
    print(post_type)


    context = {
        "comment": comment,
        "comment_fields": comment_fields,
        "post_type": post_type
    }

    return render(request, "posts/test-comment.html", context=context)
