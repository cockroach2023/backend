from pydantic_settings import BaseSettings


# 환경변수 설정
class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    ALGORITHM: str
    SECRET_KEY: str
    POSTGRES_URL: str
    REGION_NAME: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    BUCKET_NAME: str
