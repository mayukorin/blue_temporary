# Generated by Django 3.1.5 on 2021-01-16 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0028_by_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='by',
            name='comment',
        ),
        migrations.AddField(
            model_name='by',
            name='good_flag',
            field=models.BooleanField(null=True),
        ),
    ]