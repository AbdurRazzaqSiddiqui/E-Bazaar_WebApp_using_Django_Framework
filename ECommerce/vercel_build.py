"""Prepare database and static assets during a Vercel build."""

import os
import sys


REQUIRED_VERCEL_ENV = ("SECRET_KEY", "DATABASE_URL", "BLOB_READ_WRITE_TOKEN")


def enabled(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def main() -> None:
    missing = [name for name in REQUIRED_VERCEL_ENV if not os.getenv(name)]
    if os.getenv("VERCEL") and missing:
        print(
            "Vercel deployment is missing required environment variables: "
            + ", ".join(missing),
            file=sys.stderr,
        )
        raise SystemExit(1)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ECommerce.settings")

    import django
    from django.core.management import call_command

    django.setup()
    call_command("migrate", interactive=False)

    if enabled("SEED_STORE"):
        password = os.getenv("DEMO_STORE_PASSWORD", "")
        if len(password) < 12:
            print(
                "DEMO_STORE_PASSWORD must contain at least 12 characters when SEED_STORE is enabled.",
                file=sys.stderr,
            )
            raise SystemExit(1)
        call_command("seed_store", password=password)

    call_command("collectstatic", interactive=False, clear=True)


if __name__ == "__main__":
    main()
