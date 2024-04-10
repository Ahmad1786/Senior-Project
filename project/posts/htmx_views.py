from django.shortcuts import render
from django.http import Http404, HttpResponse
from posts.group_page_forms import CommentForm
from posts.models import Bill, Event, Chore
from posts.models import Post
from django.utils.timezone import get_current_timezone

is_htmx = lambda request: request.headers.get('HX-Request', False)

def add_comment(request, post_id):
    if not is_htmx(request):
        return HttpResponse(status=405)
    
    #post = Post.objects.get(pk=post_id)
    current_user = request.user
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            form.save_m2m()
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
        else:
            return render(request, 'posts/bill.html', {
                'form': form,
            })
    
    form = CommentForm()
    return render(request, 'posts/comment-form.html', {
        'form': form,
    })

def comment_box(request, post_type, post_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
        else:
            raise Http404("Form is not valid")
    else:
        initial_data = {
            # The creator of the comment.
            "author": request.user,
        }
        # Check what type of post this comment will be on and then retrieve it.
        # Store the post as a foreign key in the initial data (links the comment to the post)
        if post_type == "bill":
            initial_data["bill"] = Bill.objects.get(id=post_id)
        elif post_type == "chore":
            initial_data["task"] = Chore.objects.get(id=post_id)
        elif post_type == "event":
            initial_data["event"] = Event.objects.get(id=post_id)
        else:
            raise Http404("Error: " + post_type + " is not a valid post_type")
        
        form = CommentForm(initial=initial_data)

        return render(request, "comment-box.html", {
            "form": form,
            "post_type": post_type,
            "post_id": post_id,
        })