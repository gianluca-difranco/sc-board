from django.urls import path
from board.views import LoginView, LogoutView, BoardView

app_name = "board"

urlpatterns = [
    path("", BoardView.as_view(), name="board"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
