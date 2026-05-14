"""
Custom authentication backend per Django.
Legge dalla tabella 'users' del FastAPI e verifica la password con bcrypt,
esattamente come fa il backend FastAPI con passlib.
"""
import bcrypt
from board.models import FastApiUser


class FastApiAuthBackend:
    """
    Autentica gli utenti verificando le credenziali presenti nel DB
    condiviso con il backend FastAPI.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        username → email dell'utente.
        Restituisce l'istanza di FastApiUser se le credenziali sono valide,
        altrimenti None.
        """
        if username is None or password is None:
            return None

        try:
            user = FastApiUser.objects.get(email=username)
        except FastApiUser.DoesNotExist:
            return None

        if not user.hashed_password:
            return None

        # Verifica bcrypt — compatibile con passlib usato da FastAPI
        try:
            password_bytes = password.encode("utf-8")
            hashed_bytes = user.hashed_password.encode("utf-8")
            if bcrypt.checkpw(password_bytes, hashed_bytes):
                return user
        except Exception:
            pass

        return None

    def get_user(self, user_id):
        """Recupera l'utente dalla sessione tramite ID."""
        try:
            return FastApiUser.objects.get(pk=user_id)
        except FastApiUser.DoesNotExist:
            return None
