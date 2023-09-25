from io import BytesIO

import requests
from django.core.files import File

from web.models import Articles
from web.title_parser import get_title


def save(url, user=None):
    if not user:
        raise AttributeError("Attribute user not found")

    name = get_title(url)

    try:
        article = Articles(user=user, name=f"{name}", is_archived=False)
        args = dict(url=url, name=name)
        res = requests.get(f"http://127.0.0.1:3000/", params=args)
        article.document_file.save(f"{name}.pdf", File(BytesIO(res.content)))
        return True

    except Exception as ex:
        print(ex)
        return False
