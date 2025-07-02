from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser,SAFE_METHODS, BasePermission
from rest_framework.decorators import action
from .models import Poll, Choice, Vote
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer
from .permissions import IsOwnerOrReadOnly

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=True, methods=['get'], permission_classes=[IsAdminUser])
    def results(self, request, pk=None):

        try:
            poll = Poll.objects.get(pk=pk)
        except Poll.DoesNotExist:
            return Response({"error": "Sondaggio non trovato"}, status=status.HTTP_404_NOT_FOUND)

        results = []
        for choice in poll.choices.all():
            results.append({
                "choice": choice.choice_text,
                "votes": choice.votes.count()
            })

        return Response({
            "question": poll.question,
            "results": results
        })


class ChoiceCreateView(generics.CreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class VoteCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(voted_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ChoiceListView(generics.ListAPIView):
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        poll_id = self.request.query_params.get('poll')
        if poll_id:
            return Choice.objects.filter(poll_id=poll_id)
        return Choice.objects.all()

    class IsOwnerOrReadOnly(BasePermission):
        def has_permission(self, request, view):
            # Permetti a chi è autenticato di creare (POST)
            if request.method == 'POST':
                return request.user and request.user.is_authenticated
            # Per tutti gli altri metodi, lascia che has_object_permission gestisca
            return True

        def has_object_permission(self, request, view, obj):
            # Permetti la lettura a tutti
            if request.method in SAFE_METHODS:
                return True
            # Permetti scrittura solo al proprietario
            return obj.created_by == request.user