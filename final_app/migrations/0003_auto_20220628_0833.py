# Generated by Django 2.2.4 on 2022-06-28 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final_app', '0002_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tags',
            name='articles',
        ),
        migrations.AddField(
            model_name='articles',
            name='tag',
            field=models.CharField(default='coding', max_length=255),
        ),
    ]
