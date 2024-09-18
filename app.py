import asyncio
from typing import Sequence

import httpx
import click

import config


async def check_url(
    url: str, 
    methods: Sequence[str] = config.HTTP_METHODS,
) -> dict[str, str] | None:
    """_summary_

    Args:
        url (str)
        methods (Sequence[str], optional): 
        _description_. Defaults to config.HTTP_METHODS.

    Returns:
        dict[str, str] | None
    """
    methods = ("GET", "HEAD", "OPTIONS", "POST", "PUT", "DELETE", "PATCH")
    results = {}

    async with httpx.AsyncClient() as client:
        for method in methods:
            try:
                response = await client.request(method, url)
                if response.status_code != 405:
                    results[method] = response.status_code
            except httpx.RequestError:
                continue

    return results


async def process_urls(
    urls: Sequence[str]
) -> dict[str, dict[str, str]]:
    results = {}
    for url in urls:
        if url.startswith("http://") or url.startswith("https://"):
            results[url] = await check_url(url)
        else:
            print(f'Строка "{url}" не является ссылкой.')
    return results


@click.command()
@click.argument('urls', nargs=-1) 
def main(urls):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    results = loop.run_until_complete(process_urls(urls))
    print(results)

if __name__ == "__main__":
    main()