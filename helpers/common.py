from collections import defaultdict
import time
import functools

import discord

import sys
sys.path.append('..')

from config import RateLimitedError

request_count = defaultdict(int)
last_reset = time.monotonic()

def rate_limit(group: str, max_requests: int):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
            global last_reset
            global request_count
            
            current_time = time.monotonic()
            elapsed_time = current_time - last_reset.get(group, 0)

            if elapsed_time >= 60:
                request_count[group].clear()
                last_reset[group] = current_time

            request_count[group][interaction.user.id] += 1

            if request_count[group][interaction.user.id] > max_requests:
                raise RateLimitedError("You have been rate limit lmao", f"Please try again later. You've exceeded the rate limit for the {group} group.")
            else:
                return await func(self, interaction, *args, **kwargs)
        return wrapper
    return decorator
