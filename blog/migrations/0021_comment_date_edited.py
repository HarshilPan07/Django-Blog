# Generated by Django 3.1.1 on 2020-09-29 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_board_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date_edited',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
