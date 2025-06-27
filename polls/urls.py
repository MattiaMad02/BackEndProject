from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PollViewSet, ChoiceCreateView, VoteCreateView

router = DefaultRouter()
router.register(r'polls', PollViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('choices/', ChoiceCreateView.as_view(), name='create-choice'),
    path('vote/', VoteCreateView.as_view(), name='vote'),
]
