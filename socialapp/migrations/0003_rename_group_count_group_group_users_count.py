# Generated by Django 4.2 on 2023-08-20 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0002_group_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='group_count',
            new_name='group_users_count',
        ),
    ]