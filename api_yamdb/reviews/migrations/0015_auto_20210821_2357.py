# Generated by Django 2.2.16 on 2021-08-21 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0014_auto_20210821_2348'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title_id'), name='unique_title_author'),
        ),
    ]
