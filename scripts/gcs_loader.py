"""
GCS Loader — 將 raw SEC 數據存入 Cloud Storage
路徑格式: gs://{bucket}/sec/{ticker}/{filing_type}/{date}/{filename}.json
"""

import json
import logging
from datetime import datetime
from google.cloud import storage

logger = logging.getLogger(__name__)


class GCSLoader:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_json(self, data: dict | list, ticker: str, data_type: str, suffix: str = "") -> str:
        """
        上傳 JSON 到 GCS，回傳 gs:// URI
        
        data_type: 'submissions' | 'facts' | 'income_statement' | 'balance_sheet' | 'cash_flow'
        """
        date_str = datetime.utcnow().strftime("%Y%m%d")
        filename = f"{ticker}_{data_type}{suffix}_{date_str}.json"
        blob_path = f"sec/{ticker}/{data_type}/{date_str}/{filename}"

        blob = self.bucket.blob(blob_path)
        blob.upload_from_string(
            data=json.dumps(data, default=str, ensure_ascii=False, indent=2),
            content_type="application/json",
        )

        gcs_uri = f"gs://{self.bucket.name}/{blob_path}"
        logger.info(f"Uploaded to {gcs_uri}")
        return gcs_uri

    def upload_raw_filing_html(self, content: bytes, ticker: str, accession: str, filename: str) -> str:
        """上傳原始 10-K HTML/HTM 文件到 GCS"""
        date_str = datetime.utcnow().strftime("%Y%m%d")
        blob_path = f"sec/{ticker}/raw_filings/{date_str}/{accession}/{filename}"
        blob = self.bucket.blob(blob_path)
        blob.upload_from_string(content, content_type="text/html")
        gcs_uri = f"gs://{self.bucket.name}/{blob_path}"
        logger.info(f"Uploaded raw filing to {gcs_uri}")
        return gcs_uri
