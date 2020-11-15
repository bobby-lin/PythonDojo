import asyncio
import aiohttp
import aiofiles


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url) # Co-routines require await
        html = await response.text()
        return html


async def write_file(file, text):
    async with aiofiles.open(file, 'w') as f:
        await f.write(text)


async def main(urls):
    tasks = []
    for url in urls:
        file = f'{url.split("//")[-1]}.html'
        html = await fetch(url)
        tasks.append(write_file(file, html))

    await asyncio.gather(*tasks)


sample_urls = ['https://google.com', 'https://www.python.org', 'https://www.yahoo.com']
asyncio.run(main(sample_urls))
