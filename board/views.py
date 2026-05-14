from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from board.models import Message, Tenant


class LoginView(View):
    template_name = "board/login.html"

    def get(self, request):
        if request.session.get("user_id"):
            return redirect("board:board")
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Salva le info utente in sessione manualmente
            request.session["user_id"] = user.id
            request.session["user_email"] = user.email
            request.session["user_role"] = user.role
            request.session["tenant_id"] = user.tenant_id
            return redirect("board:board")
        else:
            messages.error(request, "Email o password non corretti.")
            return render(request, self.template_name, {"email": email})


class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect("board:login")


class BoardView(View):
    template_name = "board/board.html"

    def get(self, request):
        # Controllo autenticazione via sessione
        if not request.session.get("user_id"):
            return redirect("board:login")

        tenant_id = request.session.get("tenant_id")
        tenant_name = "FantaCalcio"

        # Recupera il nome del tenant se disponibile
        if tenant_id:
            try:
                tenant = Tenant.objects.get(pk=tenant_id)
                tenant_name = tenant.name
            except Tenant.DoesNotExist:
                pass

        # Recupera tutti i messaggi ordinati per data discendente
        board_messages = Message.objects.all()

        context = {
            "tenant_name": tenant_name,
            "messages_list": board_messages,
            "user_email": request.session.get("user_email"),
            "user_role": request.session.get("user_role"),
        }
        return render(request, self.template_name, context)
