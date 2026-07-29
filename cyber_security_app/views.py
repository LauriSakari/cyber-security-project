from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import Message

# Create your views here.

def index(request):
    return render(request, "cyber_security_app/index.html")

def bookings(request):
    return render(request, "cyber_security_app/bookings.html")

def time_slots(request):
    return render(request, "cyber_security_app/time_slots.html")


@login_required
def messages(request):
    message_list = Message.objects.select_related("user").order_by("-sent_at")
    return render(
        request,
        "cyber_security_app/messages.html",
        {
            "messages": message_list,
            "count": message_list.count(),
        },
    )


@login_required
def send_message(request):
    if request.method != "POST":
        return redirect("messages")

    content = request.POST.get("content", "").strip()
    if content:
        Message.objects.create(
            content=content,
            user=request.user,
            sent_at=timezone.now(),
        )
    return redirect("messages")


@login_required
def remove_message(request):
    if request.method != "POST":
        return redirect("messages")

    message_id = request.POST.get("remove")
    if message_id:
        Message.objects.filter(id=message_id, user=request.user).delete()
    return redirect("messages")


def register(request):
    return render(request, "cyber_security_app/register.html")


def add_user(request):
    if request.method != "POST":
        return redirect("register")

    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")
    verify_password = request.POST.get("verify_password", "")

    if not username or not password:
        return render(
            request,
            "cyber_security_app/register.html",
            {"error": "Tunnus ja salasana ovat pakollisia."},
        )

    if password != verify_password:
        return render(
            request,
            "cyber_security_app/register.html",
            {"error": "Salasanat eivät täsmää."},
        )

    if User.objects.filter(username=username).exists():
        return render(
            request,
            "cyber_security_app/register.html",
            {"error": "Käyttäjänimi on jo varattu."},
        )

    user = User.objects.create_user(username=username, password=password)
    auth_login(request, user)
    request.session["username"] = user.username
    return redirect("index")


@login_required
def profile(request):
    user_messages = Message.objects.filter(user=request.user).order_by("-sent_at")
    return render(
        request,
        "cyber_security_app/profile.html",
        {
            "user_messages": user_messages,
            "message_count": user_messages.count(),
        },
    )


def logout(request):
    auth_logout(request)
    return redirect("index")