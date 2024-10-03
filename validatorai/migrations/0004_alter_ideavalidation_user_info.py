# Generated by Django 5.1.1 on 2024-10-03 22:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validatorai', '0003_alter_ideavalidation_user_info'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='ideavalidation',
            name='user_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_idea_validation', to=settings.AUTH_USER_MODEL),
        ),
    ]
