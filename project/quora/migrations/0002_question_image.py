# Generated by Django 5.2 on 2025-04-10 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quora', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='question_images/'),
        ),
    ]
