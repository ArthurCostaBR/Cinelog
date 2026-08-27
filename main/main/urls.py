from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include("pages.urls")),
    path('accounts/', include("users.urls")),

    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
          template_name="password_reset/password_reset_form.html",
          html_email_template_name="password_reset/password_reset_email.html",
          subject_template_name="password_reset/password_reset_subject.txt",
          ), 
         name="reset_password"),

    path('password-reset-sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset/password_reset_done.html"), 
         name="password_reset_done"),

    path('password-reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset/password_reset_confirm.html"), 
         name="password_reset_confirm"),

    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset/password_reset_complete.html"), 
         name="password_reset_complete")

]