# Generated by Django 4.2 on 2023-04-14 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0006_post_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
