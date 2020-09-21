from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import migrations


def create_initialuser(apps, schema_editor):
    # Get models
    User = get_user_model()

    # Create anonymous user
    anonuser = User.objects.create(username="cisco")

    anonuser.set_password("ciscocisco")

    anonuser.save()

    # Create admin user
    adminuser = User.objects.create(
        username="admin",
        is_superuser=True,
    )

    adminuser.set_password("ciscocisco")

    adminuser.save()

    # Create hive user
    hiveuser = User.objects.create(username="snekman")

    hiveuser.set_password(settings.HIVE_PASSWORD)

    hiveuser.save()


def remove_initialuser(apps, schema_editor):
    # Get models
    User = get_user_model()

    # Delete the anonymous user
    User.objects.get(username="cisco").delete()

    # Delete the admin user
    User.objects.get(username="admin").delete()

    # Delete the hive user
    User.objects.get(username="hive").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_initialuser, remove_initialuser),
    ]
