# Generated by Django 5.1.1 on 2024-09-13 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0005_alter_customuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
