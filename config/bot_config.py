from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    token: str
    vk_api_token: str


@dataclass
class Database:
    db_name: str
    user: str
    password: str
    host: str
    port: str


def load_config():
    env = Env()
    env.read_env()
    return Config(env('TOKEN'), env('VK_API_TOKEN'))


def load_database_config():
    env = Env()
    env.read_env()
    return Database(env('db_name'), env('user'), env('password'), env('host'), env('port'))
