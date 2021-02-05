from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from leads.views import SignupView, LandingPageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('leads/', include('leads.urls', namespace='leads')),
    path('agents/', include('agents.urls', namespace='agents')),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('reset-password-done/', PasswordResetDoneView.as_view(),
         name='reset-password-done'),
    path('reset-password-complete/', PasswordResetCompleteView.as_view(),
         name='reset-password-complete'),
    path('reset-password-confirm/<uid64>/<token>',
         PasswordResetConfirmView.as_view(), name='reset-password-confrim'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
