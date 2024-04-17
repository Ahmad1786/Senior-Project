from django.shortcuts import render
from django.http import Http404, HttpResponse
from posts.group_page_forms import CommentForm
from posts.models import Bill, Event, Chore, Comment
from django.db.models import Q

is_htmx = lambda request: request.headers.get('HX-Request', False)

def get_comment_section(request, post_type, post_id):
    
    if post_type == "bill":
        post = Bill.objects.get(id=post_id)
        # Get parent comments that belong to this bill
        parent_comments =  Comment.objects.filter(Q(bill_id=post.id) & Q(parent_comment=None))
    elif post_type == "chore":
        post = Chore.objects.get(id=post_id)
        # Get parent comments that belong to this chore
        parent_comments =  Comment.objects.filter(Q(task_id=post.id) & Q(parent_comment=None))
    elif post_type == "event":
        post = Event.objects.get(id=post_id)
        # Get parent comments that belong to this event
        parent_comments =  Comment.objects.filter(Q(event_id=post.id) & Q(parent_comment=None))
    else:
        raise Http404("Error: " + post_type + " is not a valid post_type")
    
    threads = {}
    for comment in parent_comments:
        # Append the dictionary so that the key is a parent and the value contains the replies
        threads[comment] = Comment.objects.filter(parent_comment=comment)

    return render(request, "comment-section.html", {
        "post_type": post_type,
        "post_id": post_id,
        "threads": threads,
        "current_user": request.user
    })

# Used to generate a comment box to provide input and make a comment
def add_comment(request, post_type, post_id):
    if request.method == "POST":
        try:
            content = request.POST['content']
        except:
            raise ("Error, there was no value for the field \"content\" supplied.")
        
        form_data = {
            # The creator of the comment.
            "author": request.user,
            "content": content,
        }
        # Check what type of post this comment will be on and then retrieve it.
        # Store the post as a foreign key in the initial data (links the comment to the post)
        if post_type == "bill":
            form_data["bill"] = Bill.objects.get(id=post_id)
        elif post_type == "chore":
            form_data["task"] = Chore.objects.get(id=post_id)
        elif post_type == "event":
            form_data["event"] = Event.objects.get(id=post_id)
        else:
            raise Http404("Error: " + post_type + " is not a valid post_type")
        
        form = CommentForm(form_data)
        if form.is_valid():
            form.save(commit=True)
            return get_comment_section(request, post_type, post_id)
        else:
            raise Http404("Form is not valid")
    else:
        return render(request, "comment-box.html", {
            "post_type": post_type,
            "post_id": post_id,
        })
    
def add_reply(request, post_type, post_id, parent_comment_id):
    if request.method == "POST":
        try:
            content = request.POST['content']
        except:
            raise ("Error, there was no value for the field \"content\" supplied.")
        
         # The parent of the comment chain this reply will belong to
        parent_comment = Comment.objects.get(id=parent_comment_id)

        form_data = {
            # The creator of the new reply.
            "author": request.user,
            "parent_comment": parent_comment,
            "content": content,
        }
        # Check what type of post this comment will be on and then retrieve it.
        # Store the post as a foreign key in the initial data (links the comment to the post)
        if post_type == "bill":
            form_data["bill"] = Bill.objects.get(id=post_id)
        elif post_type == "chore":
            form_data["task"] = Chore.objects.get(id=post_id)
        elif post_type == "event":
            form_data["event"] = Event.objects.get(id=post_id)
        else:
            raise Http404("Error: " + post_type + " is not a valid post_type")
        
        form = CommentForm(form_data)

        if form.is_valid():
            form.save(commit=True)
            return get_comment_section(request, post_type, post_id)
        else:
            raise Http404("Form is not valid")
    else:
        return render(request, "comment-box.html", {
            "post_type": post_type,
            "post_id": post_id,
        })
    
def edit_comment(request, post_type, post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment_content = comment.content
    if request.method == "POST":
        try:
            new_content = request.POST['content']
        except:
            raise ("Error, there was no value for the field \"content\" supplied.")
        comment.content = new_content
        comment.save()
        return get_comment_section(request, post_type, post_id)
    
    return render(request, "posts/edit-comment-box.html", {
        "content": comment_content,
        "post_type": post_type,
        "post_id": post_id,
        "comment_id": comment_id,
    })
    