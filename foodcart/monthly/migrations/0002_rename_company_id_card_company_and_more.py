# Generated by Django 4.0 on 2022-01-11 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monthly', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='company_id',
            new_name='company',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='card_id',
            new_name='card',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='company_id',
            new_name='company',
        ),
    ]