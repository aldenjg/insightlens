import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
from fastapi import FastAPI, Query, HTTPException, Depends
from s3_utils import generate_presigned_post
from lambda_invoker import invoke_poller_lambda
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="InsightLens API",
    description="API for document processing and analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only Use ["http://localhost:5174"] for safer config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# config logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_aws_config():
    region = os.environ.get("AWS_REGION")
    if not region:
        logger.warning("AWS_REGION not set, defaulting to us-west-2")
        region = "us-west-2"
    return {"region_name": region}


def get_s3_client():
    return boto3.client("s3", **get_aws_config())


def get_dynamodb_resource():
    return boto3.resource("dynamodb", **get_aws_config())


def get_textract_client():
    return boto3.client("textract", **get_aws_config())


def get_lambda_client():
    return boto3.client("lambda", **get_aws_config())


def get_documents_table():
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table('insightlens-documents')


def get_search_index_table():
    dynamodb = get_dynamodb_resource()
    return dynamodb.Table('insightlens-search-index')


# API endpoints
@app.get("/health")
def health():
    """Health check endpoint for monitoring and load balancing"""
    return {"status": "healthy"}


@app.get("/search")
def search_documents(
    query: str = Query(..., description="Search term"),
    table=Depends(get_documents_table)
):
    """Search documents by extracted text content"""
    try:
        response = table.scan(
            FilterExpression=Attr("extracted_text").contains(query)
        )
        results = response.get("Items", [])
        return {"results": results}
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error searching documents"
        )


@app.get("/upload-url")
def get_upload_url():
    try:
        return generate_presigned_post()
    except Exception as e:
        logger.error(f"Error generating upload URL: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating upload URL: {str(e)}"
        )


@app.post("/poll")
def poll_textract(document_id: str, textract_job_id: str):
    """Poll Textract for job completion"""
    try:
        code = invoke_poller_lambda(document_id, textract_job_id)
        return {"status": code}
    except Exception as e:
        logger.error(f"Error polling Textract: {str(e)}")
        raise HTTPException(status_code=500, detail="Error polling Textract")


@app.get("/keyword-search")
def keyword_search(
    word: str,
    table=Depends(get_search_index_table)
):
    """Search documents by keyword"""
    try:
        response = table.query(
            KeyConditionExpression=Key('word').eq(word.lower())
        )
        return {"results": response.get("Items", [])}
    except Exception as e:
        logger.error(f"Error searching by keyword: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error searching by keyword"
        )


@app.get("/")
def root():
    return {"message": "InsightLens API is running. Visit /docs for Swagger UI."}


@app.get("/document/{document_id}")
def get_document(document_id: str, table=Depends(get_documents_table)):
    try:
        response = table.get_item(Key={"document_id": document_id})
        item = response.get("Item")
        if not item:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"document_id": item["document_id"], "text": item.get("extracted_text", "")}
    except Exception as e:
        logger.error(f"Error retrieving document: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving document")
