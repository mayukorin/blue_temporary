# Generated by Django 3.1.2 on 2021-01-07 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_correctsituation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='correct_flag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.correctsituation'),
        ),
    ]