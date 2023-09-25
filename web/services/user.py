import uuid

from web.models import User, TelegramHash


def create_telegram_auth_hash(user: User) -> TelegramHash:
    telegram_hash, created = TelegramHash.objects.get_or_create(user=user, defaults=dict(hash=uuid.uuid4()))
    return telegram_hash
