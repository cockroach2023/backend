import os
import uuid
import boto3
from app.utils.settings import Settings

settings = Settings().dict()
REGION_NAME = settings["REGION_NAME"]
AWS_ACCESS_KEY_ID = settings["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = settings["AWS_SECRET_ACCESS_KEY"]
BUCKET_NAME = settings["BUCKET_NAME"]

BUCKET_HOST = "https://{}.s3.amazonaws.com/".format(BUCKET_NAME)


def s3_connection():
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name=REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
    except Exception as e:
        raise e
    else:
        return s3


def upload_file(path, file):
    try:
        s3 = s3_connection()
        ext = file.filename.split(".")[-1]
        file_url = path
        file_url += str(uuid.uuid4())
        file_url += "." + ext

        s3.upload_fileobj(file.file, BUCKET_NAME, file_url)
        s3.close()

        return os.path.join(BUCKET_HOST, file_url)
    except Exception as e:
        raise ConnectionError(e)
