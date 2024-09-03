from typing import Optional
import os

import odmantic
import motor.motor_asyncio
from ..config import settings


engine: Optional[odmantic.AIOEngine] = odmantic.AIOEngine(
    client=motor.motor_asyncio.AsyncIOMotorClient(settings.dB.url),
    database=settings.dB.database
) if settings.dB.mode.lower() == 'db' else None
# json mode / mongodb

if engine is None:
    import ujson
    JSON_MODE: bool = True
    
    if not os.path.exists('./data/'):
        os.makedirs('./data/') # create data dir for json mode
    
else:
    JSON_MODE: bool = False