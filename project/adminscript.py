from django.contrib.auth import get_user_model
User = get_user_model()

# create a superuser
super_username = 'admin'
super_password = 'admin'
if not User.objects.filter(username=super_username).exists():
    User.objects.create_superuser(password=super_password, username=super_username, first_name='CoHabitat', last_name='Admin')
    print('Superuser created username: admin, password: admin')
else:
    print('Superuser already exists with username admin already exists')

    