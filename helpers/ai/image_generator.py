from typing import Optional, Dict, List
import random
import asyncio
from io import BytesIO

import aiohttp
from aiohttp import ClientSession

import sys
sys.path.append("...")

from config import settings

class ImageGenerator:
    base_url: str = "https://api.prodia.com"
    image_base_url: str = 'https://images.prodia.xyz/{job}.png'
    headers: Dict[str, str] = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://app.prodia.com',
        'priority': 'u=1, i',
        'referer': 'https://app.prodia.com/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    @staticmethod
    async def _start_generation(prompt: str, session: ClientSession, proxy: Optional[str] = None, **kwargs) -> str:
        params: Dict[str, str] = {
            'new': 'true',
            'prompt': prompt,
            'model': kwargs.get('model', 'absolutereality_v181.safetensors [3d9d4d2b]'),
            'negative_prompt': kwargs.get('negative_prompt', ''),
            'steps': kwargs.get('steps', '30'),
            'cfg': kwargs.get('cfg', '7'),
            'seed': kwargs.get('seed', str(random.randint(0, 2**32 - 1))),
            'sampler': kwargs.get('sampler', 'DPM++ 2M Karras'),
            'aspect_ratio': kwargs.get('aspect_ratio', 'square'),
        }

        async with session.get(ImageGenerator.base_url + '/generate', params=params, headers=ImageGenerator.headers, proxy=proxy) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data['job']
        return ""

    @staticmethod
    async def _check_job(job: str, session: ClientSession, proxy: Optional[str] = None) -> bool:
        url: str = ImageGenerator.base_url + f'/job/{job}'

        for _ in range(20):
            async with session.get(url, headers=ImageGenerator.headers, proxy=proxy) as resp:
                if resp.status != 200:
                    return False

                data = await resp.json()
                if data['status'] == 'succeeded':
                    return True

            await asyncio.sleep(1)
        return False

    @staticmethod
    async def main(prompt: str, **kwargs) -> Optional[bytes]:
        proxy = settings.proxy
        async with aiohttp.ClientSession() as session:
            job_id: str = await ImageGenerator._start_generation(prompt, session, proxy=proxy, **kwargs)
            if not job_id:
                return None

            if await ImageGenerator._check_job(job_id, session, proxy=proxy):
                url = ImageGenerator.image_base_url.format(job=job_id)

            async with session.get(url, headers=ImageGenerator.headers, proxy=proxy) as resp:
                if resp.status == 200:
                    return await resp.read()
                
        return None

if __name__ == '__main__':
    image_url: Optional[str] = asyncio.run(ImageGenerator.main('cute cat'))
    print(image_url)
