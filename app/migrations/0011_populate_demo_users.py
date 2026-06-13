from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_demo_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    
    client_group, _ = Group.objects.get_or_create(name='Client')
    manager_group, _ = Group.objects.get_or_create(name='Manager')
    
    # 1. Клиент
    client_user, created = User.objects.get_or_create(
        username='client',
        defaults={
            'password': make_password('123'),
            'is_active': True,
        }
    )
    if created:
        client_user.groups.add(client_group)
    
    # 2. Менеджер
    manager_user, created = User.objects.get_or_create(
        username='manager',
        defaults={
            'password': make_password('123'),
            'is_active': True,
            'is_staff': True, # Менеджеру дадим staff, чтобы он мог зайти в админку, если захотите
        }
    )
    if created:
        manager_user.groups.add(manager_group)
    
    # 3. Администратор (Superuser)
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'password': make_password('123'),
            'is_active': True,
            'is_staff': True,
            'is_superuser': True,
        }
    )

def reverse_func(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username__in=['client', 'manager', 'admin']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_order_orderitem'),
    ]

    operations = [
        migrations.RunPython(create_demo_users, reverse_func),
    ]
