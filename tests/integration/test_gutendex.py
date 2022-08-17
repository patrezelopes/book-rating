import json

import pytest as pytest
import requests
from starlette import status

from app.settings import settings


@pytest.mark.parametrize(
    'book_id,expected',
    [(1, 'The Declaration of Independence of the United States of America'),
     (2, 'The United States Bill of Rights: The Ten Original Amendments to the Constitution of the United States'),
     (19033, "Alice's Adventures in Wonderland")]
)
def test_get_book_by_id(book_id, expected):
    response = requests.get(f"{settings.ebook_metadata_url}/{book_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('title') == expected


@pytest.mark.parametrize(
    'title,expected',
    [('The Declaration of Independence of the United States of America', [1]),
     ('The United States Bill of Rights: The Ten Original Amendments to the Constitution of the United States', [2, 57764]),
     ("Alice's Adventures in Wonderland", [11, 19033])]
)
def test_get_book_by_id(title, expected):
    response = requests.get(f"{settings.ebook_metadata_url}/?search={title}")
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content).get('results')[0].get('id') in expected
