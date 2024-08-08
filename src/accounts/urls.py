from django.urls import path
from .views import LogoutView, CrossAuthView, onboarding_view

app_name = 'accounts'
urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('onboarding/', onboarding_view, name='onboarding'),
    path('cross-auth/', CrossAuthView.as_view(), name='cross-auth'),
]


