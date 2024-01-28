# Generated by Django 4.2.6 on 2024-01-28 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_openinghours'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openinghours',
            options={'ordering': ('day', '-from_hour')},
        ),
        migrations.AlterUniqueTogether(
            name='openinghours',
            unique_together={('vendor', 'day', 'from_hour', 'to_hour')},
        ),
    ]
