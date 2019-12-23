from typing import Union, Dict
import glob
import os
import sys

sys.path.append('..')
import config

class Icons():

    def __init__(self) -> None:
        self.abs_path = os.path.dirname(os.path.abspath(__file__))
        self.keywords_images = [[], []]
        self.images_data = {}

    def processImage(self, path) -> bool:
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
        image_info = self.formatImageInfo(path)
        keywords = self.getKeywordsFromFilename(image_info["filename"])
        if (len(keywords)):
            self.keywords_images[0].append(keywords)
            self.keywords_images[1].append(image_info["filename"])
            self.images_data[image_info["filename"]] = image_info
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
        keywords = filename
        p_filename = filename
        replace_chars="_-."
        for c in replace_chars:
            p_filename = p_filename.replace(c, " ")
        keywords += " " + p_filename
        return keywords

    def formatImageInfo(self, path) -> {"filename": str, "extension": str}:
        filename = os.path.basename(path)
        _, extension = os.path.splitext(filename)
        return {
            "filename": filename,
            "extension": extension,
        }

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
        images = []
        for icon_type in ["png", "jpeg", "jpg", "gif"]:
            uri = config.ICONS_DIRECTORY + "/*." + icon_type
            images.extend(glob.glob(uri))
        if (len(images)):
            for image_path in images:
                if (self.processImage(image_path)):
                    nb_images_processed+=1
        return nb_images_processed

    def searchImages(self, query: str, limit: 40) -> [str]:
        """
        Returns a list of images corresponding to the query.
        Breaks down the query to compute a score depending
        on the keywords previously computed.

        Args:
            query (str): The query string
            limit (int): The maximum number of images to return

        Returns:
            [{"filename": str, "extension": str}]:
                A list of images corresponding to the query.
        """
        ranking = {}
        ranking_sorted = []
        ranking_sorted_returned = []
        for key in range(0, len(self.keywords_images[0])):
            score = 0
            keywords = self.keywords_images[0][key]
            filename = self.keywords_images[1][key]
            query_tokens = query.split(' ')
            for query_token in query_tokens:
                score += 1 if (query_token in keywords) else 0
            if (score > 0):
                ranking[filename] = (ranking[filename] + 1) if (filename in ranking) else 1
        if (len(ranking) > 0):
            ranking_sorted = sorted(ranking, key=ranking.__getitem__, reverse=True)
            nb_processed = 0
            while (nb_processed < limit and nb_processed < len(ranking_sorted)):
                ranking_sorted_returned.append(ranking_sorted[nb_processed])
                nb_processed+=1
        return ranking_sorted_returned

    def getImageData(self, image_name) -> Union[Dict[str, str], None]:
        return self.images_data[image_name] if (image_name in self.images_data) else None
    
    def getImagesData(self) -> {}:
        return self.images_data
