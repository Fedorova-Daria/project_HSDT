from users.models import Account

print(Account.objects.values("id", "role"))