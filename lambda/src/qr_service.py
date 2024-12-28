import json
import os
import logging
import boto3
import segno
import requests
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3 = boto3.client('s3')

# Retrieve environment variables
BUCKET_NAME = os.getenv("BUCKET_NAME")


def lambda_handler(event, context):
    """
    Lambda entry point.
    """
    logger.info("Received event: %s", json.dumps(event))

    try:
        # Get column name and Notion token from headers
        column_name = event['headers'].get('x-column-name', 'QR Code')
        notion_token = event['headers'].get('x-notion-token')

        if not notion_token:
            raise ValueError("Missing 'x-notion-token' header")

        logger.info("Column to update: %s", column_name)

        # Parse the webhook payload
        webhook_payload = json.loads(event['body'])
        page_id = webhook_payload["data"]["id"]
        logger.info("Processing page ID: %s", page_id)

        # Generate and upload QR code
        qr_file_url = generate_qr_code_and_upload(webhook_payload)
        logger.info("Generated QR code URL: %s", qr_file_url)

        # Update the Notion page with the QR code URL
        update_notion_page(page_id, column_name, qr_file_url, notion_token)

        return {
            "statusCode": 200,
            "body": json.dumps({"status": "success"})
        }
    except Exception as e:
        logger.error("Error processing event: %s", str(e), exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"status": "error", "message": str(e)})
        }


def generate_qr_code_and_upload(webhook_payload):
    """
    Generate a QR code and upload it to S3.
    """
    page_url = webhook_payload["data"]["url"]
    page_id = webhook_payload["data"]["id"]

    # Generate the QR code image using segno
    qr = segno.make(page_url)
    temp_file_path = f"/tmp/{page_id}.png"
    qr.save(temp_file_path, scale=10)

    # Upload the QR code to S3
    try:
        s3_path = f"notion/qr/{page_id}.png"
        s3.upload_file(temp_file_path, BUCKET_NAME, s3_path)
        file_url = f"https://{BUCKET_NAME}/{s3_path}"
        logger.info("Uploaded QR code to S3: %s", file_url)
        return file_url
    except ClientError as e:
        logger.error("Error uploading QR code to S3: %s", str(e))
        raise


def update_notion_page(page_id, column_name, qr_file_url, notion_token):
    """
    Update the Notion page with the QR code URL.
    """
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {
        "properties": {
            column_name: {
                "files": [
                    {
                        "name": "QR Code",
                        "type": "external",
                        "external": {
                            "url": qr_file_url
                        }
                    }
                ]
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    response = requests.patch(url, headers=headers, data=json.dumps(payload))

    # Log response
    if response.status_code == 200:
        logger.info("QR field updated successfully: %s", response.json())
    else:
        logger.error("Error updating QR field: %d - %s", response.status_code, response.text)
        raise Exception(f"Failed to update Notion page: {response.status_code} {response.text}")