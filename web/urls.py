from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from web.views import (
    PdfAdd,
    edit_article,
    registration_view,
    login_view,
    user_page,
    logout_view,
    main,
    delete_article,
    telegram_auth_start,
    share_pdf,
    save_pdf_vue
)

urlpatterns = [
    path('api/save_pdf', save_pdf_vue),
    path("files/add", PdfAdd.as_view(), name="files_add"),
    path("registration/", registration_view, name="registration"),
    path("login/", login_view, name="login"),
    path("login/telegram/", telegram_auth_start, name="login_telegram"),
    path("user/", user_page, name="my_page"),
    path("logout/", logout_view, name="logout"),
    path("", main, name="main"),
    path("accounts/profile/", user_page),
    path("delete/<int:id_>/", delete_article, name="delete"),
    path("edit/", edit_article, name="edit"),
    path("share_pdf/", share_pdf, name="share_pdf"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
