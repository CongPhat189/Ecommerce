# Generated by Django 5.1.5 on 2025-02-04 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0009_alter_like_active_alter_like_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('seller', 'Seller'), ('user', 'User')], default='user', max_length=10),
        ),
    ]
