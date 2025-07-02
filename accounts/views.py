from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

User = get_user_model()

class RegisterUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Username e password richiesti"}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Utente già esistente"}, status=400)
        user = User.objects.create_user(username=username, password=password)
        # Assegna il gruppo "AuthenticatedUsers"
        group, _ = Group.objects.get_or_create(name="AuthenticatedUsers")
        user.groups.add(group)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"message": "Utente registrato correttamente", "token":token.key}, status=201)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    return Response({
        "username": request.user.username,
        "is_superuser": request.user.is_superuser
    })
