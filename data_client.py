import aiohttp

async def send_request_async(session: aiohttp.ClientSession, url: str, headers, form_data: aiohttp.FormData, time_out: int = 60):
    try:
        async with session.post(url=url, headers=headers, data=form_data, timeout=aiohttp.ClientTimeout(total=time_out)) as response:
            await response.text()
            response.raise_for_status()
            return response
    except Exception as e:
        print(f'ERROR: send_request_async - {e}')
        raise