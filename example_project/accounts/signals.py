from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

try:
    from articles.models import Comment
except Exception:
    Comment = None


@receiver(post_migrate)
def create_default_groups(sender, **kwargs) -> None:
    if Comment is None:
        return

    author_group, _ = Group.objects.get_or_create(name="author")
    moderator_group, _ = Group.objects.get_or_create(name="moderator")
    comment_ct = ContentType.objects.get_for_model(Comment)
    add_comment = Permission.objects.get(codename="add_comment",
                                         content_type=comment_ct)
    change_comment = Permission.objects.get(codename="change_comment",
                                            content_type=comment_ct)
    delete_comment = Permission.objects.get(codename="delete_comment",
                                            content_type=comment_ct)
    author_group.permissions.set({add_comment, change_comment})
    moderator_group.permissions.set(
        {add_comment, change_comment, delete_comment})
