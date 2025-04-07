from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int 
    JWT_SECRET_KEY: str
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    API_KEY: str
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()