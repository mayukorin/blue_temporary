# Generated by Django 3.1.5 on 2021-01-13 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0026_auto_20210109_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, null=True)),
                ('evaluation_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation', to='app1.type')),
            ],
        ),
        migrations.CreateModel(
            name='By',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evaluation_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='by_for_evalution', to='app1.evaluationtag')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='by_for_problem', to='app1.problem')),
                ('site_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='by_for_site_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
