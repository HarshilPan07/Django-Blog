# Generated by Django 3.1.1 on 2020-09-27 06:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_remove_comment_replies'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='date_created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]