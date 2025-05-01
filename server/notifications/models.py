from django.db import models
from users.models import Account  # Импортируем модель пользователя Account

class Notification(models.Model):
    # Тип уведомления (например, 'team_member_added', 'team_join_request_accepted')
    notification_type = models.CharField(max_length=255)
    
    # Сообщение уведомления (например, "Вас добавили в команду")
    message = models.TextField()
    
    # Пользователь, которому предназначено уведомление
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='notifications')
    
    # Статус уведомления (например, 'new', 'read')
    status = models.CharField(max_length=50, default='new')
    
    # Дата и время создания уведомления
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.notification_type}"
    
    class Meta:
        ordering = ['-created_at']
