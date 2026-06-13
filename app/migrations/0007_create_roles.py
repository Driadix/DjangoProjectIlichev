from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='Client')
    Group.objects.get_or_create(name='Manager')


def reverse_func(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Client', 'Manager']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_blog_to_news'),
    ]

    operations = [
        migrations.RunPython(create_groups, reverse_func),
    ]
