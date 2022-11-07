from pathlib import Path
from typing import Iterable
from .document import Document
import json
from io import StringIO

class JsonFileDocument(Document):
    """
    Represents a document that is saved as a JSON in the local file system.
    """
    def __init__(self, id : int, path : Path):
        super().__init__(id)
        self.path = path
        self._name = path.name
        with open(path, 'r') as file:
            data = json.load(file)
            self._title = data["title"]


    @property
    def title(self) -> str:
        return self._title

    @property
    def name(self) -> str:
        return self._name

    # returns TextIOWrapper
    def get_content(self) -> Iterable[str]:
        with open(self.path, 'r') as file:
            data = json.load(file)
        return StringIO(data["body"])

    @staticmethod
    def load_from(abs_path : Path, doc_id : int) -> 'JsonFileDocument' :
        """A factory method to create a JsonFileDocument around the given file path."""
        return JsonFileDocument(doc_id, abs_path)
