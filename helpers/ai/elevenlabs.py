import aiohttp, asyncio


import sys
sys.path.append('...')

from config import settings

class ElevenLabs:
    """
    Provider class for interacting with the ElevenLabs API.
    """
    elevenlabs_voice_map = {
        "alice": "Xb7hH8MSUJpSbSDYk0k2",
        "bill": "pqHfZKP75CvOlQylNhV4",
        "brian": "nPczCjzI2devNBz1zQrb",
        "callum": "N2lVS1w4EtoT3dr4eOWO",
        "charlie": "IKne3meq5aSn9XLyUdCD",
        "charlotte": "XB0fDUnXU5powFXDhCwa",
        "chris": "iP95p4xoKVk53GoZ742B",
        "daniel": "onwK4e9ZLuTAKqWW03F9",
        "george": "JBFqnCBsd6RMkjVDRZzb",
        "liam": "TX3LPaxmHKxFdv7VOQHJ",
        "lily": "pFZP5JQG7iQjIQuC4Bku",
        "matilda": "XrExE9yKIg1WjnnlVkGX"
    }
    
    headers = {'accept': '*/*','accept-language': 'en-US,en;q=0.9','content-type': 'application/json','origin': 'https://elevenlabs.io','priority': 'u=1, i','referer': 'https://elevenlabs.io/','sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-site','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}

    @classmethod
    async def speech(cls, prompt: str, voice: str) -> bytes:
        """Creates an audio speech using the ElevenLabs API."""

        async with aiohttp.ClientSession() as session:
            for i in range(5):
                async with session.post(
                    url=f"https://api.elevenlabs.io/v1/text-to-speech/{cls.elevenlabs_voice_map.get(voice, cls.elevenlabs_voice_map['callum'])}?allow_unauthenticated=1",
                    proxy=settings.proxy,
                    json={
                        "model_id": "eleven_turbo_v2_5",
                        "text": prompt[:500]
                    },
                    headers=cls.headers
                ) as response:
                    try:
                        response.raise_for_status()
                        audio_bytes = await response.read()
                    except aiohttp.ClientError:
                        if i != 4:
                            continue
                        else:
                            raise ValueError
        return audio_bytes
