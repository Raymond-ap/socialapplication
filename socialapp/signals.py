# models.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *

@receiver(post_save, sender=Follow)
def update_follower_following_count(sender, instance, **kwargs):
    

    user1 = User.objects.get(id=instance.follower.id)
    user2= User.objects.get(id=instance.following.id)

   
    follower_following_count = user1.following_count
    following_follower_count = user2.follower_count
   
    if user1:
        instance.follower.following_count = follower_following_count + 1
        instance.follower.save()

    if user2:
        instance.following.follower_count = following_follower_count + 1
        instance.following.save()
    



@receiver(post_delete, sender=Follow)
def update_follower_following_count_on_delete(sender, instance, **kwargs):
    user1 = instance.follower
    user2 = instance.following

    if user1:
        user1.following_count = user1.following_count - 1
        user1.save()

    if user2:
        user2.follower_count = user2.follower_count - 1
        user2.save()



@receiver(post_save, sender=PostInteraction)
def update_post_interaction(sender, instance, created, **kwargs):
    if created:
        
        post = instance.post
        interaction_type = instance.interaction_type

        if interaction_type == PostInteraction.COMMENT and instance.interaction_text:
            post.interaction_count += 1
            post.save()
        elif interaction_type == PostInteraction.LIKE:
            post.interaction_count += 1
            post.save()
