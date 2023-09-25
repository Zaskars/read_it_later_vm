from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from read_it_later.settings import TELEGRAM_BOT_LOGIN
from web.forms import PdfForm, UserRegistrationForm, AuthForm, EditForm
from web.models import Articles, User
from web.services.user import create_telegram_auth_hash
from web.tasks import save_pdf


def main(request):
    if request.user.is_authenticated:
        return redirect("files_add")
    return redirect("registration")


@login_required
def share_pdf(request):
    if request.method == "GET":
        url = request.GET.get("url")
        try:
            save_pdf.delay(url=url, user_id=request.user.id)
        except Exception as ex:
            print(ex)
            return False
        return redirect('my_page')


class PdfAdd(LoginRequiredMixin, View):
    @staticmethod
    def _render(request, form=None, message=None):
        return render(request, "web/add_article.html", {"form": form or PdfForm(), "message": message})

    def get(self, request):
        return self._render(request, {'user': request.user})


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def save_pdf_vue(request):
    data = request.data
    user = User.objects.all().filter(email=data['user'])[0]

    if user:
        save_pdf.delay(url=data['url'], user_id=user.id)
        return Response({'status': 'success'})

    return Response({'status': 'error'})


def registration_view(request):
    form = UserRegistrationForm()

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            del cleaned_data["password2"]
            new_user = User.objects.create_user(**cleaned_data)
            login(request, new_user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("files_add")

    return render(request, "web/registration.html", {"form": form})


def login_view(request):
    form = AuthForm(request.POST or None)
    message = None

    if request.method == "POST":
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                message = "Почта или пароль неправильные"
            else:
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                next_url = "files_add"

                if "next" in request.GET:
                    next_url = request.GET.get("next")

                return redirect(next_url)

    return render(request, "web/login.html", {"form": form, "message": message})


@login_required
def telegram_auth_start(request):
    telegram_hash = create_telegram_auth_hash(request.user)
    login = TELEGRAM_BOT_LOGIN
    hash = telegram_hash.hash
    return redirect(f"https://t.me/{login}?start={hash}")


@login_required
def logout_view(request):
    logout(request)
    return redirect("registration")


@login_required
def user_page(request):
    articles = Articles.objects.filter(user=request.user)
    return render(request, "web/user_page.html", {"articles": articles})


@login_required
def delete_article(request, id_):
    try:
        article = Articles.objects.get(user=request.user, id=id_)
        article.delete()
        return redirect("my_page")
    except:
        return redirect("my_page")


@login_required
def edit_article(request):
    user = User.objects.get(id=request.user.id)
    form = EditForm(initial={"new_email": user.email, "new_name": user.name})
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data["new_email"]
            user.name = form.cleaned_data["new_name"]
            if form.cleaned_data["new_password"]:
                user.set_password(form.cleaned_data["new_password"])
                user.save()
                return redirect("login")
            else:
                user.save()
                return redirect("my_page")
    return render(request, "web/edit.html", {"user": user, "form": form})
