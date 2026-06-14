from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    db_url: str = Field(..., alias='NEON_CONNECTION_STRING')
    redis_url: str = Field(..., alias='REDIS_URL')
    s3_url: str = Field(..., alias='LOCALSTACK_S3_URL')
    bucket_name: str = Field(..., alias='S3_BUCKET_NAME')
    aws_access: str = Field(..., alias='AWS_ACCESS_KEY_ID')
    aws_secret_access: str = Field(..., alias='AWS_SECRET_ACCESS_KEY')
    aws_region: str = Field(..., alias='AWS_REGION')
    model_config = SettingsConfigDict(env_file=".env")

settings = Setting() # type: ignore