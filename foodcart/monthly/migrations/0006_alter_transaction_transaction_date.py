# Generated by Django 4.0 on 2022-01-13 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monthly', '0005_alter_transaction_options_alter_company_funds_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]