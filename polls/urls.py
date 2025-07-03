from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PollViewSet, ChoiceCreateView, VoteCreateView, ChoiceViewSet
from .views import ChoiceListView
router = DefaultRouter()
router.register(r'polls', PollViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('choices/create/', ChoiceCreateView.as_view(), name='create-choice'),
    path('vote/', VoteCreateView.as_view(), name='vote'),
    path('choices/', ChoiceListView.as_view(), name='choice-list'),
]
