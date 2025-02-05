# Generated by Django 5.1.5 on 2025-02-04 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0008_like_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'product')},
        ),
    ]
