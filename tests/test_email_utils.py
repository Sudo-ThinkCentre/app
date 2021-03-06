from app.email_utils import (
    get_email_name,
    get_email_part,
    get_email_local_part,
    get_email_domain_part,
    email_belongs_to_alias_domains,
    can_be_used_as_personal_email,
)
from app.extensions import db
from app.models import User, CustomDomain


def test_get_email_name():
    assert get_email_name("First Last <ab@cd.com>") == "First Last"
    assert get_email_name("First Last<ab@cd.com>") == "First Last"
    assert get_email_name("  First Last   <ab@cd.com>") == "First Last"
    assert get_email_name("ab@cd.com") == ""


def test_get_email_part():
    assert get_email_part("First Last <ab@cd.com>") == "ab@cd.com"
    assert get_email_part("First Last<ab@cd.com>") == "ab@cd.com"
    assert get_email_part("  First Last   <ab@cd.com>") == "ab@cd.com"
    assert get_email_part("ab@cd.com") == "ab@cd.com"


def test_get_email_local_part():
    assert get_email_local_part("ab@cd.com") == "ab"


def test_get_email_domain_part():
    assert get_email_domain_part("ab@cd.com") == "cd.com"


def test_email_belongs_to_alias_domains():
    # default alias domain
    assert email_belongs_to_alias_domains("ab@sl.local")
    assert not email_belongs_to_alias_domains("ab@not-exist.local")

    assert email_belongs_to_alias_domains("hey@d1.test")
    assert not email_belongs_to_alias_domains("hey@d3.test")


def test_can_be_used_as_personal_email(flask_client):
    # default alias domain
    assert not can_be_used_as_personal_email("ab@sl.local")
    assert not can_be_used_as_personal_email("hey@d1.test")

    assert can_be_used_as_personal_email("hey@ab.cd")
    # custom domain
    user = User.create(
        email="a@b.c", password="password", name="Test User", activated=True
    )
    db.session.commit()
    CustomDomain.create(user_id=user.id, domain="ab.cd", verified=True)
    db.session.commit()
    assert not can_be_used_as_personal_email("hey@ab.cd")
