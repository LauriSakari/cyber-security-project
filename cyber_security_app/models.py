from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
	content = models.TextField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	sent_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		db_table = "messages"

