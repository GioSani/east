from django.db.models.signals import pre_save
from django.dispatch import receiver
from core.models import User

# @receiver(post_save,sender=settings.AUTH_USER_MODEL)
# def group(sender,instance,created,**kwargs):
#         group = Group.objects.get(name='myauthors')
#         if instance.is_blog_author == True:
#            instance.groups.add(group)
#         elif instance.is_blog_author == False:
#              instance.groups.remove(group) 




@receiver(pre_save, sender=User)
def my_handler(sender, **kwargs):
    print('signal is handled=======')