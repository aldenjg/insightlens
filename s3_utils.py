import boto3
import uuid
import os


region = os.environ.get("AWS_REGION", "us-west-2")

lambda_client = boto3.client("lambda", region_name=region)
s3 = boto3.client("s3", region_name=region)
dynamodb = boto3.resource("dynamodb", region_name=region)

s3 = boto3.client("s3")
BUCKET_NAME = "insightlens-docs-bucket"


def generate_presigned_post():
    document_id = str(uuid.uuid4())
    key = f"uploads/{document_id}.pdf"

    url = s3.generate_presigned_post(
        Bucket=BUCKET_NAME,
        Key=key,
        Fields={"acl": "private", "Content-Type": "application/pdf"},
        Conditions=[
            {"acl": "private"},
            {"Content-Type": "application/pdf"}
        ],
        ExpiresIn=3600
    )
    return {"document_id": document_id, "upload_url": url}
