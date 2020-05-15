# Generated by Django 3.0.5 on 2020-05-13 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20200508_1615'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'categories', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AddField(
            model_name='restaurant',
            name='logo',
            field=models.ImageField(default='002.jpg', upload_to='logos', verbose_name='Логотип Ресторана'),
        ),
    ]