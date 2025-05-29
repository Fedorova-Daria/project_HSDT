from django.db import models
from users.models import Account
from core.models import Technology, Semester
from teams.models import Team
from django.conf import settings
import json

class Institute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('review', 'На рассмотрении'),
        ('open', 'В поиске'),
        ('in_progress', 'В работе'),
        ('under_revision', 'На доработке'),
        ('done', 'Сделан'),
    ]

    DURATION_CHOICES = [
        ("semester", "1 семестр"),
        ("year", "1 год"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.ManyToManyField(Technology, blank=True)
    institutes = models.CharField(max_length=255, blank=True, default='[]')

    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='projects_owned')
    initiator = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='projects_initiated', blank=True, null=True)

    teams = models.ManyToManyField(Team, related_name='projects', blank=True)
    workers = models.ManyToManyField(Account, related_name='workers_projects', blank=True)

    favorites = models.ManyToManyField(Account, related_name="favorite_projects", blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    visible = models.BooleanField(default=False)  # Для модерации
    votes_to_approve = models.PositiveIntegerField(default=3)
    approved = models.BooleanField(default=False)

    likes = models.ManyToManyField(Account, related_name="liked_projects", blank=True)
    expert_likes = models.ManyToManyField(Account, related_name="expert_liked_projects", blank=True)

    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True)

    def get_institutes_list(self):
        try:
            return json.loads(self.institutes)
        except:
            return []

    def set_institutes_list(self, inst_list):
        self.institutes = json.dumps(inst_list)

    def check_approval(self):
        if self.expert_likes.count() >= self.votes_to_approve:
            self.approved = True
            self.visible = True
            self.status = "open"
            self.save()

    def __str__(self):
        return self.title
    
    def get_average_rating_for_user(self, user):
        ratings = self.participant_ratings.filter(rated_user=user)
        if ratings.exists():
            return round(ratings.aggregate(models.Avg('rating'))['rating__avg'], 2)
        return None

class ProjectMessage(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_revision_request = models.BooleanField(default=False)

class ProjectParticipantRating(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='participant_ratings')
    rated_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='ratings_received')
    rated_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='ratings_given')

    rating = models.PositiveSmallIntegerField()  # например, от 1 до 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rated_by} → {self.rated_user} ({self.rating}) in {self.project}"



class Idea(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('open', 'Опубликован'),
        ('under_review', 'На согласовании'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.ManyToManyField(Technology, related_name="ideas_with", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='ideas')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    visible = models.BooleanField(default=False)

    likes = models.ManyToManyField(Account, related_name="liked_ideas", blank=True)
    expert_likes = models.ManyToManyField(Account, related_name="experts_liked_ideas", blank=True)

    def __str__(self):
        return self.title


# projects/models.py

class ProjectApplication(models.Model):
    APPLICANT_TYPE_CHOICES = (
        ('freelancer', 'Фрилансер'),
        ('team', 'Команда'),
    )

    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
        ('cancelled', 'Отменено'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    applicant_type = models.CharField(max_length=20, choices=APPLICANT_TYPE_CHOICES)
    freelancer = models.ForeignKey(Account, null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
