# Generated by Django 4.1.2 on 2022-11-23 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='receipient',
            new_name='recipient',
        ),
    ]
