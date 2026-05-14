"""
Modelli Django che mappano le tabelle esistenti del FastAPI backend.
managed=False → Django non crea né migra queste tabelle.
"""
from django.db import models


class FastApiUser(models.Model):
    """
    Mappa la tabella 'users' del backend FastAPI.
    Usato solo per la sessione di autenticazione Django.
    """
    id = models.AutoField(primary_key=True)
    tenant_id = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)
    hashed_password = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=10)  # AS, TA, TU

    class Meta:
        managed = False
        db_table = "users"

    def __str__(self):
        return self.email

    # Attributi richiesti da Django per il sistema di autenticazione
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"


class Tenant(models.Model):
    """Mappa la tabella 'tenants' per recuperare il nome del fantacalcio."""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=7, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "tenants"

    def __str__(self):
        return self.name


class Message(models.Model):
    """
    Mappa la tabella 'message' creata dalla Lambda lambda_write_db.py.
    """
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=False)

    class Meta:
        managed = False
        db_table = "message"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Message #{self.id} @ {self.created_at}"
