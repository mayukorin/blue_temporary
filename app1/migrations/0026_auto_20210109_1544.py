# Generated by Django 3.1.2 on 2021-01-09 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0025_auto_20210109_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='problem_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to='app1.problem_group'),
        ),
    ]
