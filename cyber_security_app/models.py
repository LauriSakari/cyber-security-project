from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")


class Message(models.Model):
	content = models.TextField(null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	sent_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		db_table = "messages"


class Location(models.Model):
	name = models.TextField(null=True, blank=True)

	class Meta:
		db_table = "locations"


class FreeTime(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)
	date_of_time = models.DateField(null=True, blank=True)
	start_time = models.TimeField()
	end_time = models.TimeField()

	class Meta:
		db_table = "free_times"
		constraints = [
			models.CheckConstraint(
				condition=models.Q(start_time__lt=models.F("end_time")),
				name="check_time",
			),
		]


class BookedTime(models.Model):
	free_time = models.ForeignKey(FreeTime, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		db_table = "booked_times"
		constraints = [
			models.UniqueConstraint(
				fields=["free_time", "user"],
				name="booked_times_pk",
			),
		]


User.add_to_class(
	"booked_times",
	models.ManyToManyField(
		FreeTime,
		through=BookedTime,
		related_name="booked_users",
		blank=True,
	),
)
