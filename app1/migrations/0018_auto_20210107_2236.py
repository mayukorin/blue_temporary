# Generated by Django 3.1.2 on 2021-01-07 13:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0017_auto_20210107_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='solve_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='solve_plan_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]