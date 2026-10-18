import json

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import SubscriberForm
from .models import Subscriber

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
def api_waitlist(request):
    """JSON API для React: POST {"email": "..."} -> 200 {"status": "added" | "exists"}."""
    try:
        data = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Невірний JSON."}, status=400)

    email = str(data.get("email", "")).strip().lower()
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"error": "Невірна адреса пошти."}, status=400)

    try:
        _, created = Subscriber.objects.get_or_create(email=email)
    except IntegrityError:
        # Хтось одночасно додав ту саму адресу.
        created = False
    return JsonResponse({"status": "added" if created else "exists"})
