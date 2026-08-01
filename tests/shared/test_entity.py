from hios.shared.entity import Entity


class User(Entity):
    name: str


def test_entity_has_id():
    user = User(name="John")

    assert user.id is not None


def test_entity_has_audit():
    user = User(name="John")

    assert user.audit.created_at is not None


def test_entities_have_unique_ids():
    user1 = User(name="John")
    user2 = User(name="Jane")

    assert user1.id != user2.id