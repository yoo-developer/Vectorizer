import os
import cuid
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError

# Load Wasabi credentials securely
WASABI_ACCESS_KEY = os.getenv("WASABI_ACCESS_KEY")
WASABI_SECRET_KEY = os.getenv("WASABI_SECRET_KEY")
WASABI_ENDPOINT = "s3.us-west-1.wasabisys.com"

# Initialize S3 client
S3 = boto3.client(
    "s3",
    aws_access_key_id=WASABI_ACCESS_KEY,
    aws_secret_access_key=WASABI_SECRET_KEY,
    endpoint_url=f"https://{WASABI_ENDPOINT}",
)

def upload_markup(markup: str, s3_bucket_name: str) -> str | None:
    """Uploads an SVG markup to Wasabi and returns the file key."""
    cuid_str = cuid.cuid()
    
    try:
        S3.put_object(
            Body=markup.encode("utf-8"),
            Bucket=s3_bucket_name,
            Key=cuid_str,
            ContentType="image/svg+xml",
            ContentDisposition="inline",  # Helps browsers display SVG properly
        )
        return cuid_str

    except (BotoCoreError, NoCredentialsError) as e:
        print(f"Upload failed: {e}")
        return None

def get_object_url(s3_file_key: str, s3_bucket_name: str) -> str | None:
    """Retrieves a public URL for a stored object if it exists."""
    try:
        S3.head_object(Bucket=s3_bucket_name, Key=s3_file_key)
        
        return S3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": s3_bucket_name, "Key": s3_file_key},
        ).split("?")[0]

    except S3.exceptions.NoSuchKey:
        print(f"File {s3_file_key} not found in bucket {s3_bucket_name}.")
        return None
    except (BotoCoreError, NoCredentialsError) as e:
        print(f"Failed to get object URL: {e}")
        return None

def upload_file(local_file_path: str, s3_bucket_name: str, s3_file_key: str) -> str | None:
    """Uploads a local file to Wasabi and returns the file's public URL."""
    try:
        S3.upload_file(local_file_path, s3_bucket_name, s3_file_key)
        return get_object_url(s3_file_key, s3_bucket_name)

    except (BotoCoreError, NoCredentialsError) as e:
        print(f"File upload failed: {e}")
        return None
