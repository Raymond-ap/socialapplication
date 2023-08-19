# models.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *

@receiver(post_save, sender=Follow)
def update_follower_following_count(sender, instance, **kwargs):
    follower_count = instance.follower.follower_count
    following_count = instance.following.following_count

    user1 = User.objects.get(id=instance.follower.id)
    user2= User.objects.get(id=instance.following.id)

    print("follower_count", follower_count, "following_count", following_count)

    if user1:
        instance.follower.following_count = following_count + 1
        instance.follower.save()

    if user2:
        instance.following.follower_count = follower_count + 1
        instance.following.save()


@receiver(post_save, sender=PostInteractionType)
def update_post_interaction(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        interaction_type = instance.interaction_type

        if interaction_type == PostInteractionType.COMMENT and instance.interaction_text:
            # If it's a comment interaction, update interaction text and count
            post.interaction_count += 1
            post.save()
        elif interaction_type == PostInteractionType.LIKE:
            # If it's a like interaction, update interaction count
            post.interaction_count += 1
            post.save()
