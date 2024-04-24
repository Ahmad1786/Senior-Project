from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .forms import SwapOfferForm
from posts.models import Bill, Event, Chore, SwapOffer, SwapRequest
from servers.models import Server, Participation, Invitation
from django.utils.timezone import get_current_timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# some quick server side validation
# was trying to see if I could use a decorator for ease but those are complicated
is_htmx = lambda request: request.headers.get('HX-Request', False)
can_edit = lambda user, post: user == post.creator

def swap_request(request, task_id):
    if not is_htmx(request):
        return HttpResponse(status=405)
    
    chore_instance = Chore.objects.get(pk=task_id)
    context = {
        "chore": chore_instance
    }
    
    if request.method == 'POST':
        SwapRequest.create_swap_request(chore_instance, request.user)
        context['success'] = True
    
    return render(request, 'servers/partials/swap-request-modal.html', context=context)

@require_POST
def create_swap_offer(request, swap_request_id):
    swap_request = SwapRequest.objects.get(pk=swap_request_id)
    form = SwapOfferForm(request.POST, user=request.user, swap_request=swap_request)
    request_server = swap_request.chore.server
    all_swap_requests = SwapRequest.objects.filter(chore=swap_request.chore, status='PENDING').exclude(id=swap_request_id)
    print(all_swap_requests)
    if form.is_valid():
        # Extract form data
        offer_chore = form.cleaned_data['offer_chore']
        status = form.cleaned_data['status']
        print(offer_chore)
        print(status)
        # Create the swap offer
        current_offer=SwapOffer.create_offer(swap_request=swap_request, offer_chore=offer_chore, status='PENDING', user=request.user)
        if status == 'ACCEPTED' and offer_chore != None:
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
        elif status == 'ACCEPTED' and offer_chore==None:
            current_offer.accept_offer()
            for swap_request_left in all_swap_requests:
                SwapOffer.create_offer(swap_request=swap_request_left, offer_chore=None, status="DECLINED", user=request.user)
            return HttpResponse(status=204, headers={'HX-Trigger': 'PageRefreshNeeded'})
        else:
            current_offer.decline_offer()
        return JsonResponse({'status': 'success'}, status=200)
    
def manage_swap_request(request, swap_request_id):
    if not is_htmx(request):
        return HttpResponse(status=405)
    
    swap_request_instance = SwapRequest.objects.get(pk=swap_request_id)
    print(swap_request_instance)
    swap_request_offers = SwapOffer.objects.filter(swap_request=swap_request_instance)
    
    if request.method == 'POST':
        if 'accept_swap_offer' in request.POST:
            offer_id = request.POST.get('accept_swap_offer')
            offer = SwapOffer.objects.get(pk=offer_id)
            offer.accept_offer()
            return HttpResponse(status=204)
        elif 'decline_swap_offer' in request.POST:
            offer_id = request.POST.get('decline_swap_offer')
            offer = SwapOffer.objects.get(pk=offer_id)
            offer.decline_offer()
            return HttpResponse(status=204)
    if request.method == 'DELETE':
            swap_request_instance.delete()
            context = {'DoneDelete': True}
    else:
        # Get user display names from Participation model
        user_display_names = Participation.objects.filter(
            server=swap_request_instance.chore.server
        ).values_list('user__id', 'display_name')

        context = {
            "swap_request_instance": swap_request_instance,
            "swap_request_offers": swap_request_offers,
            "user_display_names": dict(user_display_names)
        }
    
    return render(request, 'servers/partials/manage-swap-request.html', context)

def swap_offer(request, task_id):
    task = get_object_or_404(Chore, pk=task_id)
    swap_requests = SwapRequest.objects.filter(chore=task, status='PENDING')

    # Creating a list of tuples to hold forms for each swap request
    swap_request_forms = [(swap_request, SwapOfferForm(user=request.user, swap_request=swap_request)) for swap_request in swap_requests]

    context = {
        'swap_requests': swap_requests,
        'swap_request_forms': swap_request_forms,
    }
    print(swap_request_forms)
    return render(request, 'servers/partials/swap-offer-form.html', context)


@csrf_exempt
@require_POST
def decline_swap_offer(request, offer_id):
    try:
        offer = SwapOffer.objects.get(pk=offer_id)
        offer.decline_offer()
        return JsonResponse({'status': 'success'}, status=200)
    except SwapOffer.DoesNotExist:
        return JsonResponse({'status': 'not found'}, status=404)   

@csrf_exempt
@require_POST
def accept_swap_offer(request, offer_id):
    offer = SwapOffer.objects.get(pk=offer_id)
    offer.accept_offer()
    return JsonResponse({'status': 'success'}, status=200)