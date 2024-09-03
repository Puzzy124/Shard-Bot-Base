from collections import defaultdict
import discord
import time
import functools

last_reset = {}
request_count = defaultdict(lambda: defaultdict(int))

def rate_limit(group: str, max_requests: int):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
            global last_reset
            global request_count
            
            current_time = time.monotonic()
            
            if group not in last_reset:
                last_reset[group] = current_time
            
            elapsed_time = current_time - last_reset[group]
            if elapsed_time >= 60:
                request_count[group].clear()
                last_reset[group] = current_time

            request_count[group][interaction.user.id] += 1

            if request_count[group][interaction.user.id] > max_requests:
                await interaction.response.send_message(f"Rate limit exceeded. Please try again later.", ephemeral=True)
                return
            else:
                return await func(self, interaction, *args, **kwargs)
        return wrapper
    return decorator