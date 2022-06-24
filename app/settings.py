import os

DATABASE_URL: str = os.getenv("DATABASE_URL")
SERVER_PORT: str = os.getenv("SERVER_PORT")

SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY")
S3_BUCKET: str = os.getenv("S3_BUCKET")