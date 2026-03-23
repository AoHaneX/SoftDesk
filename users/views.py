from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [AllowAny] #to Del

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]
    

    """Pour un projet final RGPD/sécurité, on limitera ensuite :

la liste de tous les utilisateurs ;

l’accès à ses propres données ;

la suppression/modification à soi-même.

Mais pour cette étape pédagogique, ce ModelViewSet permet bien de :

créer ;

lire ;

modifier ;

supprimer un utilisateur.
"""