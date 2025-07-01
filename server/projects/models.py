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
    
INSTITUTE_NAMES = {
    'HSDT': 'ВШЦТ',
    'ARHID': 'АРХИД',
    'IPTI' : 'ИПТИ',
    'STROIN' : 'СТРОИН'
}

class Project(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('review', 'На рассмотрении'),
        ('open', 'В поиске'),
        ('in_progress', 'В работе'),
        ('under_revision', 'На доработке'),
        ('done', 'Сделан'),
        ('new', 'Новый'),
        ('under_revision_on_admin', 'На доработке дирекции')
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

    teams = models.ManyToManyField(Team, related_name='projects_team', blank=True)
    workers = models.ManyToManyField(Account, related_name='workers_projects', blank=True)

    favorites = models.ManyToManyField(Account, related_name="favorite_projects", blank=True)

    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='draft')

    visible = models.BooleanField(default=False)  # Для модерации
    votes_to_approve = models.PositiveIntegerField(default=3)
    approved = models.BooleanField(default=False)

    likes = models.ManyToManyField(Account, related_name="liked_projects", blank=True)
    expert_likes = models.ManyToManyField(Account, related_name="expert_liked_projects", blank=True)

    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_teams_working_on(self):
        return self.teams.all()  # Возвращает все команды, работающие над проектом

    def get_institutes_list(self):
        try:
            return json.loads(self.institutes)
        except:
            return []

    @property
    def institutes_verbose(self):
        codes = self.get_institutes_list()
        return [INSTITUTE_NAMES.get(code, code) for code in codes]

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
    sender_role = models.CharField(
    max_length=20,
    choices=[('expert', 'Expert'), ('admin', 'Admin'), ('user', 'User')],
    null=True,
    blank=True  # Опционально, если используешь формы
)
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
        ('private', 'Приватная'),
        ('under_review', 'На согласовании'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.ManyToManyField(Technology, related_name="ideas_with", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='ideas')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True,related_name='ideas_team')  # Связь с командой

    visible = models.BooleanField(default=False)

    likes = models.ManyToManyField(Account, related_name="liked_ideas", blank=True)
    expert_likes = models.ManyToManyField(Account, related_name="experts_liked_ideas", blank=True)

    # Связь с командами, которые работают над идеей
    teams_working_on = models.ManyToManyField(Team, related_name="ideas_working_on", blank=True)


    def __str__(self):
        return self.title

    def is_visible_to_user(self, user):
        """Проверяет, может ли пользователь видеть идею."""
        if self.status == "open" or "draft" or "under_review":
            return True
        elif self.status == "private":
            # Проверяем доступ для приватных идей
            if self.team:
                # Доступ есть у:
                # 1. Участников команды
                # 2. Пользователей с ролью EXPERT
                # 3. Владельца идеи
                return (user in self.team.members.all() or
                        user.role == Account.Role.EXPERT or
                        user == self.owner)
            else:
                # Если идея приватная, но не привязана к команде
                # Доступ есть только у владельца и экспертов
                return user == self.owner or user.role == Account.Role.EXPERT
        return False

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
