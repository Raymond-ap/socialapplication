# Generated by Django 4.2 on 2023-08-19 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0002_alter_follow_follower_alter_follow_following'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='interraction_count',
            new_name='interaction_text',
        ),
    ]
