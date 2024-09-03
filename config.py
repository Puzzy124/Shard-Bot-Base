import os
from typing import Optional
import pydantic
import pydantic_settings
import pydantic_settings_yaml

class Database(pydantic.BaseModel):
    """
    Represents the database section in the configuration file.
    """

    url: str
    database: str
    mode: str
    
class Settings(pydantic_settings_yaml.YamlBaseSettings):
    """
    Private information and settings
    """
    dB: Database
    token: str
    proxy: Optional[str] = None
    
    model_config = pydantic_settings.SettingsConfigDict(
        yaml_file=os.path.abspath(os.path.join(os.path.dirname(__file__), "config.yml")),
        yaml_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
settings: Settings = Settings()

class RateLimitedError(Exception):
    def __init__(self, title: str, body: str):
        super().__init__(body)
        self.title = title
        self.body = body
