from rest_framework import generics, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action
from .models import Poll, Choice, Vote
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer
from .permissions import IsOwnerOrReadOnly, IsChoiceOwnerOrReadOnly

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
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

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, IsChoiceOwnerOrReadOnly]

class ChoiceCreateView(generics.CreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class VoteCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        user = request.user
        poll_id = request.data.get("poll")
        choice_id = request.data.get("choice")

        # Verifica che il sondaggio esista
        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            return Response({"error": "Sondaggio non trovato."}, status=status.HTTP_404_NOT_FOUND)

        # Verifica che la scelta appartenga a quel sondaggio
        try:
            choice = Choice.objects.get(id=choice_id, poll=poll)
        except Choice.DoesNotExist:
            return Response({"error": "Scelta non valida per questo sondaggio."}, status=status.HTTP_400_BAD_REQUEST)

        # Controllo che l'utente non abbia già votato per questo sondaggio
        if Vote.objects.filter(user=user, poll=poll).exists():
            return Response({"error": "Hai già votato per questo sondaggio."}, status=status.HTTP_409_CONFLICT)

        # Crea il voto
        vote = Vote(user=user, poll=poll, choice=choice)
        vote.save()

        serializer = VoteSerializer(vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class ChoiceListView(generics.ListAPIView):
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        poll_id = self.request.query_params.get('poll')
        if poll_id:
            return Choice.objects.filter(poll_id=poll_id)
        return Choice.objects.all()