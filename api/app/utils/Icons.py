from typing import Union, Dict, List
import os
import sys
from operator import countOf
from .utils import list_rglob_files

sys.path.append('..')
import config


class Icons():

    def __init__(self) -> None:
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.keywords_images = [[], []]
        self.images_data = {}

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
        keywords = self.getKeywordsFromFilename(image_info["path"])
        if (len(keywords)):
            self.keywords_images[0].append(keywords)
            self.keywords_images[1].append({
                "id": image_info["id"],
                "filename": image_info["filename"]
            })
            self.images_data[image_info["id"]] = image_info
            return True
        return False

    def getKeywordsFromFilename(self, filename) -> str:
        """
        Deducts the image's keywords from its filename.

        Args:
            filename (str): The image's filename

        Returns:
            str: The image's keywords separated by a whitespace.
        """
        keywords_str = filename
        p_filename = filename
        replace_chars="_-./"
        for c in replace_chars:
            p_filename = p_filename.replace(c, " ")
        keywords_str += " " + p_filename + " " + p_filename.lower() + " " + p_filename.upper()
        keywords = keywords_str.split(' ')
        keywords.append(keywords_str)
        return keywords

    def updateImages(self) -> int:
        """
        We look into /icons to find images to present
        to the user and deduct its keywords for search.

        Returns:
            int: The number of images successfuly processed.
        """
        self.keywords_images = [[], []]
        self.images_data = {}
        nb_images_processed = 0
        images = list_rglob_files(config.ICONS_DIRECTORY, [
            "*.png",
            "*.jpeg",
            "*.jpg",
            "*.gif",
            "*.svg"
        ])
        if (len(images)):
            for image_details in images:
                if (self.processImage(image_details)):
                    nb_images_processed+=1
        return nb_images_processed

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
        for key in range(0, len(self.keywords_images[0])):
            score = 0
            keywords = self.keywords_images[0][key]
            file_hash = self.keywords_images[1][key]["id"]
            query_tokens = query.split(' ')
            for query_token in query_tokens:
                score += countOf(keywords, query_token) + keywords[0].count(query_token)
                score += 1 if query_token in keywords[0] else 0
            if (score > 0):
                ranking[file_hash] = (ranking[file_hash] + score) if (file_hash in ranking) else score
        if (len(ranking) > 0):
            ranking_sorted = sorted(ranking, key=ranking.__getitem__, reverse=True)
            nb_processed = 0
            while (nb_processed < limit and nb_processed < len(ranking_sorted)):
                ranking_sorted_returned.append(self.filterImageData(
                    self.images_data[ranking_sorted[nb_processed]]
                ))
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
