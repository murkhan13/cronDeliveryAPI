# Generated by Django 3.0.8 on 2020-08-01 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0022_auto_20200801_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='feedbacksAmount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='sumOfPoints',
            field=models.IntegerField(default=0),
        ),
    ]