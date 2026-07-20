"""Remove the disposable records created during deployment verification."""

from django.db import migrations
from django.db.models import Q


VERIFICATION_USERNAMES = (
    "codex_preview_verify_20260720a",
    "codex_preview_seller_20260720a",
)
VERIFICATION_EMAILS = (
    "codex-preview-verify-20260720a@example.com",
    "codex-preview-seller-20260720a@example.com",
)


def remove_verification_data(apps, schema_editor):
    database = schema_editor.connection.alias
    User = apps.get_model("EBazaar", "User")
    Order = apps.get_model("EBazaar", "Order")
    Product = apps.get_model("EBazaar", "Product")

    users = User.objects.using(database).filter(
        Q(username__in=VERIFICATION_USERNAMES) | Q(email__in=VERIFICATION_EMAILS)
    )
    user_ids = list(users.values_list("pk", flat=True))

    # Order.user and Product.seller are protected relationships, so remove
    # those disposable objects before deleting their verification accounts.
    Order.objects.using(database).filter(user_id__in=user_ids).delete()
    Product.objects.using(database).filter(
        Q(sku="CODEX-VERIFY-20260720A") | Q(seller_id__in=user_ids)
    ).delete()
    users.delete()


class Migration(migrations.Migration):
    dependencies = [("EBazaar", "0019_commerce_rebuild")]

    operations = [
        migrations.RunPython(remove_verification_data, migrations.RunPython.noop),
    ]
