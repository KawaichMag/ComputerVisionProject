from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/cv_project"
    SECRET_KEY: str = "secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PHOTO_FOLDER_FULL_NAME: str = "~/Python_projects/cv_project/photos"
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()