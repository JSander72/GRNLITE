#!/usr/bin/env python
"""
Debug server script to help identify 500 errors in production
"""
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line


def debug_server():
    """Run debug checks for the server"""

    print("🔍 GRNLITE Debug Information")
    print("=" * 50)

    # Set up Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grnlite.settings")
    django.setup()

    print("✅ Django setup successful")

    # Check environment variables
    print("\n📝 Environment Variables:")
    critical_vars = [
        "DJANGO_SECRET_KEY",
        "DATABASE_URL",
        "DEBUG",
        "DJANGO_ALLOWED_HOSTS",
        "NODE_ENV",
    ]

    for var in critical_vars:
        value = os.getenv(var)
        if value:
            # Don't show sensitive values
            if "SECRET" in var or "PASSWORD" in var:
                print(f"   {var}: {'*' * len(value)} (Set)")
            else:
                print(f"   {var}: {value}")
        else:
            print(f"   {var}: ❌ NOT SET")

    # Check database connection
    print("\n💾 Database Connection:")
    try:
        from django.db import connection

        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("   ✅ Database connection successful")
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")

    # Check static files
    print("\n📁 Static Files:")
    print(f"   STATIC_URL: {settings.STATIC_URL}")
    print(f"   STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"   STATICFILES_DIRS: {settings.STATICFILES_DIRS}")

    # Check if static files exist
    import glob

    static_files = glob.glob(os.path.join(settings.STATIC_ROOT, "*"))
    print(f"   Static files count: {len(static_files)}")

    # Check templates
    print("\n📄 Templates:")
    for template_config in settings.TEMPLATES:
        for template_dir in template_config["DIRS"]:
            print(f"   Template dir: {template_dir}")
            if os.path.exists(template_dir):
                template_files = os.listdir(template_dir)
                print(f"   Template files: {len(template_files)}")
            else:
                print(f"   ❌ Template dir does not exist")

    # Check apps
    print("\n📱 Installed Apps:")
    for app in settings.INSTALLED_APPS:
        print(f"   {app}")

    print("\n🔍 Debug complete!")


if __name__ == "__main__":
    debug_server()
