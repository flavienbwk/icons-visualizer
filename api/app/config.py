import os

FLASK_SERVER_NAME = "Icons Visualizer"
FLASK_SERVER_DESCRIPTION = "A dockerized icons visualizer to find any image by keyword that can be used offline."
USE_S3 = True if os.environ.get("USE_S3", "false") == "true" else False
ICONS_DIRECTORY = "/icons"
ICONS_S3_DIRECTORY = "/icons_s3"
IMAGE_EXTENSIONS = [
    "*.png",
    "*.jpeg",
    "*.jpg",
    "*.gif",
    "*.svg"
]