from django.test import TestCase
from freezegun import freeze_time
from django.utils import timezone
from posts.models import RecurringTask, Chore
from users.models import User
from servers.models import Server

# Create your tests here.
class RecurringTaskTest(TestCase):

    @freeze_time("2024-01-01")
    def test_recurring_task_creation_over_a_week(self):
        server = Server.objects.create(group_name="Test Server")
        user = User.objects.create_user(username="testuser", password="testpass")
        creator = User.objects.create_user(username="creator", password="creatorpass")

        recurring_task = RecurringTask.objects.create(
            server=server,
            title="Test Task",
            description="This is a test task",
            first_due_date=timezone.now() + timezone.timedelta(days=3), # first due on 2024-01-04
            recurring_period=3, # Every 3 day
            recurring_unit='day',
            creator=creator
        )
        recurring_task.assignee.add(user)

        # run check_and_create_chore every day for 7 days
        week = [
            "2024-01-01",
            "2024-01-02",
            "2024-01-03",
            "2024-01-04",
            "2024-01-05",
            "2024-01-06",
            "2024-01-07",
            "2024-01-08",
            "2024-01-09",
            "2024-01-10",
        ]

        # simulate the passing of time
        for point in week:
            with freeze_time(point):
                recurring_task.check_and_create_chore()

        correct_due_dates = [
            "2024-01-04",
            "2024-01-07",
            "2024-01-10",
            "2024-01-13",
        ]

        correct_created_dates = [
            "2024-01-01",
            "2024-01-04",
            "2024-01-07",
            "2024-01-10",
        ]
  
        for chore, due_date in zip(Chore.objects.all(), correct_due_dates):
            self.assertEqual(str(chore.due_date), due_date)

        for chore, created_date in zip(Chore.objects.all(), correct_created_dates):
            self.assertEqual(str(chore.date_created)[0:10], created_date)
                