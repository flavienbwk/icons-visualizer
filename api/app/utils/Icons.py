from typing import Union, Dict, List
import os
import sys
import time
import traceback
from operator import countOf
from .utils import list_rglob_files, create_directory, remove_directory
from .Minio import Minio

sys.path.append('..')
import config


CACHE_LAST_RUN = 0.0
CACHE_EXPIRATION_INTERVAL = 120.0 # Seconds before re-processing images keywords

class Icons:

    def __init__(self) -> None:
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.keywords_images = [[], []]
        self.images_data = {}
        self.keyword_delimiters=" _-./()"

    def processImage(self, image_info) -> bool:
        """
        Finds keywords and image info from its path
        and stores them in the classe's attributes.

        Args:
            path (str): The path to the locally located image.

        Returns:
            bool: 
                True if the processing of the image succeeded.
                False otherwise.
        """
        keywords = self.getKeywordsFromFileInfo(image_info)
        if (len(keywords)):
            self.keywords_images[0].append(keywords)
            self.keywords_images[1].append({
                "id": image_info["id"],
                "filename": image_info["filename"]
            })
            self.images_data[image_info["id"]] = image_info
            return True
        return False

    def getKeywordsFromFileInfo(self, image_info) -> List:
        """
        Deducts the image's keywords from its filename, path, extension...

        Args:
            image_info (object): The image details

        Returns:
            list: The image keywords
        """
        keywords = []
        parts = [
            image_info["path"],
            image_info["filename"],
            image_info["filename"],
            image_info["filename"].lower(),
            image_info["filename"].upper()
        ]

        parts_str = ' '.join(parts)
        for delimiter in self.keyword_delimiters:
            keywords = keywords + parts_str.split(delimiter)
        
        return keywords

    def downloadImagesFromS3(self) -> int:
        """
        If USE_S3 is true, downloads all icons from the "icons"
        bucket and save them under `/icons/s3`.

        Returns:
            int: The number of images successfuly saved.
        """
        nb_images_processed = 0
        if config.USE_S3:
            try:
                minio = Minio()
                remove_directory(config.ICONS_S3_DIRECTORY)
                create_directory(config.ICONS_S3_DIRECTORY)
                buckets = [ bucket.name for bucket in minio.client.list_buckets() ]
                if "icons" in buckets:
                    print("Downloading S3 files...", flush=True)
                    objects = list(minio.client.list_objects("icons", recursive=True))
                    filenames = [ item._object_name for item in objects ]
                    for filename in filenames:
                        dst_path = f"{config.ICONS_S3_DIRECTORY}/{filename}"
                        minio.client.fget_object("icons", filename, dst_path)
                    nb_images_processed = len(filenames)
                    print(f"Finished downloading {nb_images_processed} S3 files.", flush=True)
                else:
                    minio.client.make_bucket("icons")
            except Exception as e:
                print(traceback.format_exc())
                print("ERROR: Failed to retrieve files from Minio", e)
        return nb_images_processed

    def processImageKeywords(self):
        """
        We look into `/icons` to find images to present
        to the user and deduct its keywords for search.

        Returns:
            int: The number of images successfuly processed.
        """
        print("Loading icon keywords...", flush=True)
        nb_images_processed = 0
        images = list_rglob_files(config.ICONS_DIRECTORY, config.IMAGE_EXTENSIONS)
        if config.USE_S3:
            images = images + list_rglob_files(config.ICONS_S3_DIRECTORY, config.IMAGE_EXTENSIONS)
        if (len(images)):
            for image_details in images:
                if (self.processImage(image_details)):
                    nb_images_processed+=1
        print("Finished with {} icons.".format(
            len(self.getImagesData())
        ), flush=True)
        return nb_images_processed

    def updateImages(self) -> int:
        """
        Will successively retrieve S3 images if enabled and
        keywords of images in `/icons`.

        Returns:
            int: The number of images successfuly processed.
        """
        global CACHE_LAST_RUN
        global CACHE_EXPIRATION_INTERVAL
        
        # Re-process keywords only after a specific period of time
        if time.time() - CACHE_LAST_RUN > CACHE_EXPIRATION_INTERVAL:
            CACHE_LAST_RUN = time.time()
            self.keywords_images = [[], []]
            self.images_data = {}
            self.downloadImagesFromS3()
            return self.processImageKeywords()
        return 0

    def searchImages(self, query: str, limit: 50) -> List[str]:
        """
        Returns a list of images corresponding to the query.
        Breaks down the query to compute a score depending
        on the keywords previously computed.

        Args:
            query (str): The query string
            limit (int): The maximum number of images to return

        Returns:
            [{"id": str, "filename": str, "extension": str}]:
                A list of images corresponding to the query.
        """
        ranking = {}
        ranking_sorted = []
        ranking_sorted_returned = []

        # Browse each file keywords and compute their matching
        # score for the search query submitted.
        self.updateImages()
        for key in range(0, len(self.keywords_images[0])):
            score = 0
            keywords = self.keywords_images[0][key]
            file_hash = self.keywords_images[1][key]["id"]
            query_tokens = query.split(' ')
            for query_token in query_tokens:
                score += countOf(keywords, query_token)
                score += keywords[len(keywords) - 1].count(query_token)
            if (score > 0):
                ranking[file_hash] = (ranking[file_hash] + score) if (file_hash in ranking) else score

        # If match are found, sort them by score
        if (len(ranking) > 0):
            ranking_sorted = sorted(ranking, key=ranking.__getitem__, reverse=True)
            nb_processed = 0
            while (nb_processed < limit and nb_processed < len(ranking_sorted)):
                returned_data = self.images_data[ranking_sorted[nb_processed]]
                ranking_sorted_returned.append(self.filterImageData(returned_data))
                nb_processed+=1
        return ranking_sorted_returned

    def filterImageData(self, image_data):
        return {
            "id": image_data["id"],
            "filename": image_data["filename"],
            "extension": image_data["extension"]
        }

    def getImageData(self, image_hash) -> Union[Dict[str, str], None]:
        return self.images_data[image_hash] if (image_hash in self.images_data) else None
    
    def getImagesData(self) -> Dict[str, str]:
        return self.images_data
