from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser
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
        """
        Solo i superuser possono vedere i risultati.
        Accessibile via: /polls/<id>/results/
        """
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
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class VoteCreateView(APIView):
    permission_classes = [AllowAny]  # Anche utenti anonimi possono votare

    def post(self, request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            voted_by_user = request.user if request.user.is_authenticated else None
            serializer.save(voted_by=voted_by_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

