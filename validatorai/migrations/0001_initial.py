# Generated by Django 5.1.1 on 2024-09-13 13:02

import django.db.models.expressions
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IdeaValidation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_idea', models.TextField(default='')),
                ('user_target_market', models.CharField(max_length=200)),
                ('bot_response', models.TextField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('user_info', models.ForeignKey(on_delete=django.db.models.expressions.Case, related_name='user_idea_validation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
