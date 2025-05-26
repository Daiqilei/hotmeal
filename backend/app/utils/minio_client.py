"""
File Name:        minio_client.py
Project:          backend
Author:           taichilei
Organization:     taichilei
Date Created:     2025-04-18
Description:      <文件描述信息>
"""
import uuid
from minio import Minio
from werkzeug.utils import secure_filename
from flask import current_app
import os
from dotenv import load_dotenv

load_dotenv()

client = Minio(
    endpoint=os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=os.getenv("MINIO_SECURE") == "true"
)

bucket_name = os.getenv("MINIO_BUCKET")

def upload_to_minio(file, folder="avatar"):
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[-1]
    object_name = f"{folder}/{uuid.uuid4().hex}.{ext}"

    # 若桶不存在就创建
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    client.put_object(
        bucket_name=bucket_name,
        object_name=object_name,
        data=file.stream,
        length=-1,
        part_size=10 * 1024 * 1024,
        content_type=file.mimetype,
    )

    return f"http://{os.getenv('MINIO_ENDPOINT')}/{bucket_name}/{object_name}"