from django.shortcuts import render
from .forms import SubscriberForm

def subscribe(request):
    form = SubscriberForm(request.POST or None)
    saved = False
    if form.is_valid():
        form.save()
        saved = True
        form = SubscriberForm()
    return render(request, "users/subscribe.html", {"form": form, "saved": saved})

# Create your views here.
