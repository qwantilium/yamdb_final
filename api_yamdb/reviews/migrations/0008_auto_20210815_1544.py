# Generated by Django 2.2.16 on 2021-08-15 15:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20210815_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genretitle',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='titles_by_genre', to='reviews.Genre'),
        ),
        migrations.AlterField(
            model_name='genretitle',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genres_of_title', to='reviews.Title'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
