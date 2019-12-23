from typing import Dict, Union

class ApiResponse():
    """
    A class that formats correctly the expected
    response from the web applicaiton.
    """

    def __init__(self) -> None:
        self.error = True
        self.message = ""
        self.details = {}

    def setAll(self, error: bool, message: str, details: dict) -> None:
        self.error = error
        self.message = message
        self.details = details

    def setError(self, error: bool) -> None:
        self.error = error
    
    def setMessage(self, message: str) -> None:
        self.message = message

    def setDetails(self, details: dict) -> None:
        self.details = details

    def getResponse(self) -> {"error": bool, "message": str, "details": {}}:
        return {
            "error": self.error,
            "message": self.message,
            "details": self.details
        }
