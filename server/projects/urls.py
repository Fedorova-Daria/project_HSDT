from django.urls import path
from .views import IdeaListView, IdeaDetailView, VoteIdeaView, IdeaCreateView

urlpatterns = [
    path("ideas/", IdeaListView.as_view(), name="ideas-list"),
    path("ideas/<int:pk>/", IdeaDetailView.as_view(), name="idea-detail"),
    path("ideas/<int:idea_id>/vote/", VoteIdeaView.as_view(), name="idea-vote"),
    path("ideas/create/", IdeaCreateView.as_view(), name="idea-create"),
]
