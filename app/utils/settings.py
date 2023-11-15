from pydantic_settings import BaseSettings


# 환경변수 설정
class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    ALGORITHM: str
    SECRET_KEY: str
    POSTGRES_URL: str
