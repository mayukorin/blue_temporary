# Generated by Django 3.1.2 on 2021-01-09 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0024_auto_20210109_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='correct_situation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.correctsituation'),
        ),
    ]
