# Generated by Django 3.1.2 on 2021-01-06 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_answer_comment_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteuser',
            name='reference_user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
