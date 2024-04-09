from posts.models import RecurringTask

def my_scheduled_job():
    for rt in RecurringTask.objects.all():
        rt.check_and_create_chore()