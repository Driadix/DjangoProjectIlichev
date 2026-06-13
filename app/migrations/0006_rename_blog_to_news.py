from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_update_images'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Blog',
            new_name='News',
        ),
        migrations.AlterModelOptions(
            name='news',
            options={
                'ordering': ['-posted'],
                'verbose_name': 'новость',
                'verbose_name_plural': 'новости',
            },
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={
                'ordering': ['-date'],
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'комментарии к новостям',
            },
        ),
    ]
