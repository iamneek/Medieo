import boto3
from config import settings

client = boto3.client("s3", endpoint_url=settings.s3_url)


def s3_transcoded_upload(file_path, key):
    try:
        client.upload_file(file_path, settings.bucket_name, key)
    except Exception as e:
        raise RuntimeError(f"S3 upload failed: {e}")


def s3_get_presigned_url(key, expiry=3600):
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.bucket_name, "Key": key},
        ExpiresIn=expiry,
    )
