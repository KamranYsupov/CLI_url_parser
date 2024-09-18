import pytest
from app import check_url


async def test_check_url():
    url = "https://httpbin.org/get"
    result = await check_url(url)
    assert "GET" in result
    assert result["GET"] == 200


async def test_invalid_url():
    url = "invalid_url"
    result = await check_url(url)
    assert result == {}


async def test_multiple_methods():
    url = "https://httpbin.org/anything"
    result = await check_url(url)
    assert "GET" in result or "POST" in result 
