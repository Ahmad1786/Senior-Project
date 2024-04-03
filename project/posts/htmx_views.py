from django.shortcuts import render
from django.http import HttpResponse
from posts.group_page_forms import CommentForm
from posts.models import Bill, Event, Chore
from posts.models import Post
from django.utils.timezone import get_current_timezone

is_htmx = lambda request: request.headers.get('HX-Request', False)

def add_comment(request, post_id):
    if not is_htmx(request):
        return HttpResponse(status=405)
    post = Post.objects.get(pk=post_id)
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST, current_user=current_user)
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