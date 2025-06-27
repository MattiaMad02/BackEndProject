from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class RegisterUser(APIView):
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

        return Response({"message": "Utente registrato correttamente"}, status=201)

