# Generated by Django 3.1.2 on 2021-01-01 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_auto_20210101_1956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Similar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromProblem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.problem')),
            ],
        ),
    ]
