# Generated by Django 4.2.6 on 2023-10-21 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('author', models.TextField()),
                ('publisher_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('content', models.TextField()),
                ('news_url', models.CharField(max_length=300)),
                ('image_url', models.CharField(max_length=300)),
                ('hashvalue', models.CharField(blank=True, max_length=300)),
            ],
            options={
                'db_table': 'news',
            },
        ),
    ]
