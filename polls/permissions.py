from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Permette a chiunque di fare richieste di sola lettura (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Per le richieste di scrittura serve autenticazione
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Per metodi "sicuri" (lettura) permette a tutti
        if request.method in permissions.SAFE_METHODS:
            return True
        # Per metodi scrittura solo il creatore o superuser
        return obj.created_by == request.user or request.user.is_superuser
class IsChoiceOwnerOrReadOnly(permissions.BasePermission):
    """
    Permette la modifica di una scelta solo al creatore del sondaggio o a un superuser.
    """
    def has_object_permission(self, request, view, obj):
        # Permetti operazioni di sola lettura a chiunque
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permetti modifica solo al creatore del sondaggio o al superuser
        return obj.poll.created_by == request.user or request.user.is_superuser
