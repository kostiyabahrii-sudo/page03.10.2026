import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import SubscriberForm

def subscribe(request):
    form = SubscriberForm(request.POST or None)
    saved = False
    if form.is_valid():
        form.save()
        saved = True
        form = SubscriberForm()
    return render(request, "users/subscribe.html", {"form": form, "saved": saved})


@csrf_exempt
@require_POST
def api_subscribe(request):
    """JSON API для React: POST {"email": "..."} -> 201 або 400 з помилками."""
    try:
        data = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"errors": {"__all__": ["Невірний JSON."]}}, status=400)

    form = SubscriberForm(data)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    subscriber = form.save()
    return JsonResponse(
        {"id": subscriber.id, "email": subscriber.email},
        status=201,
    )
