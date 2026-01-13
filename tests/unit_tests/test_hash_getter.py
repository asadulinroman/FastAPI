import hashlib

import pytest

from app.infrastructure.hash_getter import HashGetter


@pytest.mark.anyio
async def test_get_hash(tmp_path):
    test_image_content = b'test_content'
    test_hash = hashlib.md5(test_image_content).hexdigest()

    test_image = tmp_path / 'test_image.jpg'
    test_image.write_bytes(test_image_content)

    hash_getter = HashGetter()
    result_hash = await hash_getter.get_hash(str(test_image))

    assert result_hash == test_hash


