# Generated by Django 4.1.2 on 2022-10-23 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_post_desc_alter_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='', unique=True),
        ),
    ]
