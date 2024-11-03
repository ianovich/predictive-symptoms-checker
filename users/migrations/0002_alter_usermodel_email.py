# Generated by Django 5.0.1 on 2024-02-03 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with that email address already exists.'}, max_length=254, unique=True),
        ),
    ]
