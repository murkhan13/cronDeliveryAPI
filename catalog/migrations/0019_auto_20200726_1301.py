# Generated by Django 3.0.8 on 2020-07-26 10:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0018_auto_20200726_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='likedUsers',
            field=models.ManyToManyField(related_name='favoriteRestaurants', to=settings.AUTH_USER_MODEL),
        ),
    ]