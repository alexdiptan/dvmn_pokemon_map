# Generated by Django 3.1.14 on 2023-06-03 12:18

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0012_auto_20230603_1135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='evolution_from',
        ),
        migrations.AddField(
            model_name='pokemon',
            name='previous_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_evolution', to='pokemon_entities.pokemon'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='appeared_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 3, 12, 18, 32, 259735, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='disappeared_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 3, 12, 18, 32, 259747, tzinfo=utc)),
        ),
    ]
