from django.db import models
from users.models import Account


class offers(models.Model): 
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('open', 'Опубликован'),
        ('review', 'На рассмотрении')
    ]

    OFFER_TYPE_CHOICES = [
        ('toir', 'ТОИР'),
        ('other', 'Прочее'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='offer')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, default='other')

    likes = models.ManyToManyField(Account, related_name="liked_offers", blank=True)

    def __str__(self):
        return self.title