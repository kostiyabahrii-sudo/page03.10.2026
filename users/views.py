import json

from django.core import signing
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


SURVEY_SALT = "waitlist-survey"
SURVEY_MAX_AGE = 60 * 60  # the survey token is valid for one hour
OTHER_MAX_LENGTH = 200


def _read_json(request):
    """Parsed JSON object from the request body, or None if it isn't one."""
    try:
        data = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


@csrf_exempt
@require_POST
def api_waitlist(request):
    """JSON API для React: POST {"email": "..."}.

    -> 200 {"status": "added" | "exists", "survey_token": "..." | null}

    survey_token дозволяє одразу після цього відправити відповідь на
    "How did you hear about us?" (api_waitlist_source). Він є лише поки
    людина ще не відповіла.
    """
    data = _read_json(request)
    if data is None:
        return JsonResponse({"error": "Невірний JSON."}, status=400)

    email = str(data.get("email", "")).strip().lower()
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"error": "Невірна адреса пошти."}, status=400)

    try:
        subscriber, created = Subscriber.objects.get_or_create(email=email)
    except IntegrityError:
        # Хтось одночасно додав ту саму адресу.
        subscriber, created = Subscriber.objects.get(email=email), False

    survey_token = None
    if subscriber.heard_from == Subscriber.Source.NONE:
        survey_token = signing.dumps(subscriber.pk, salt=SURVEY_SALT)
    return JsonResponse(
        {"status": "added" if created else "exists", "survey_token": survey_token}
    )


@csrf_exempt
@require_POST
def api_waitlist_source(request):
    """POST {"token": "...", "source": "friend|social|ai|other", "other": "..."}

    Зберігає відповідь на "How did you hear about us?". Хто нічого не
    відповів, лишається в базі зі значенням "none".
    """
    data = _read_json(request)
    if data is None:
        return JsonResponse({"error": "Невірний JSON."}, status=400)

    try:
        subscriber_id = signing.loads(
            str(data.get("token", "")), salt=SURVEY_SALT, max_age=SURVEY_MAX_AGE
        )
    except signing.BadSignature:  # also covers an expired token
        return JsonResponse({"error": "Невірний або прострочений токен."}, status=400)

    source = data.get("source")
    answers = [c for c in Subscriber.Source.values if c != Subscriber.Source.NONE]
    if source not in answers:
        return JsonResponse({"error": "Невірний варіант відповіді."}, status=400)

    other = ""
    if source == Subscriber.Source.OTHER:
        other = str(data.get("other", "")).strip()[:OTHER_MAX_LENGTH]

    updated = Subscriber.objects.filter(pk=subscriber_id).update(
        heard_from=source, heard_from_other=other
    )
    if not updated:
        return JsonResponse({"error": "Не знайдено."}, status=404)
    return JsonResponse({"status": "saved"})
