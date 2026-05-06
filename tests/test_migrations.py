import pytest
from django.core.management import call_command


class TestMigrations:
    @pytest.mark.django_db
    def test_all_necessary_migrations_created(self):
        try:
            call_command("makemigrations", "--check", "--dry-run")
            all_necessary_migrations_created = True
        except SystemExit:
            all_necessary_migrations_created = False
        assert all_necessary_migrations_created
