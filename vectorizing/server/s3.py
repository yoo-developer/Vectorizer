import cuid
import boto3
import os

# Get Wasabi credentials from environment variables
WASABI_ACCESS_KEY = os.getenv('WASABI_ACCESS_KEY')
WASABI_SECRET_KEY = os.getenv('WASABI_SECRET_KEY')
WASABI_REGION = os.getenv('WASABI_REGION', 'us-east-1')  # Default to us-east-1 if not specified

# Create S3 client with Wasabi endpoint
S3 = boto3.client(
    "s3",
    endpoint_url=f"https://s3.{WASABI_REGION}.wasabisys.com",
    aws_access_key_id=WASABI_ACCESS_KEY,
    aws_secret_access_key=WASABI_SECRET_KEY,
    region_name=WASABI_REGION
)

def upload_markup (markup, s3_bucket_name):
    cuid_str = cuid.cuid()

    S3.put_object(
        Body = markup.encode('utf-8'),
        Bucket = s3_bucket_name,
        Key = cuid_str,
        ContentType = "image/svg+xml",
    )

    return cuid_str

def get_object_url(s3_file_key, s3_bucket_name):
    try:
        S3.get_object(
            Key=s3_file_key,
            Bucket=s3_bucket_name
        )

    except(Exception):
        return None

    return S3.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": s3_bucket_name, "Key": s3_file_key},
    ).split("?")[0]

def upload_file(
    local_file_path,
    s3_bucket_name,
    s3_file_key,
):
    S3.upload_file(
        local_file_path,
        s3_bucket_name,
        s3_file_key,
    )
    return get_object_url(s3_file_key, s3_bucket_name)
