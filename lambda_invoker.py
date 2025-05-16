import os
import boto3

region = os.environ.get("AWS_REGION", "us-west-2")

lambda_client = boto3.client("lambda", region_name=region)
s3 = boto3.client("s3", region_name=region)
dynamodb = boto3.resource("dynamodb", region_name=region)

def invoke_poller_lambda(document_id, textract_job_id):
    payload = {
        "document_id": document_id,
        "textract_job_id": textract_job_id
    }

    response = lambda_client.invoke(
        FunctionName="textractPoller",
        InvocationType="RequestResponse",
        Payload=bytes(str(payload), encoding="utf-8"),
    )

    return response['StatusCode']
