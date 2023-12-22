# Generated by Django 4.2.6 on 2023-11-26 16:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_news_image_url_alter_news_news_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='last_modified',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='news',
            name='publisher_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
