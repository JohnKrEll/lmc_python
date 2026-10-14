from enum import Enum
from pathlib import Path


class LMC_FileType(Enum):
    MACHINE_CODE = 0
    ASSEMBLY = 1


class LMC_FileReader:
    """
    Creates a Filereader object for LMC Program Text Files.

    - path: The path to the file this should hold.
    """

    def __init__(self, path):
        self._path = Path(path)
        with self._path.open() as f:
            first_line = f.readline()
        self._filetype = self._detect(first_line)

    # Detects the filetype of the program file
    def _detect(self, line: str) -> LMC_FileType:
        if line.isnumeric():
            return LMC_FileType.MACHINE_CODE
        return LMC_FileType.ASSEMBLY

    # Returns the filetype as LMC_FileType. 
    def get_filetype(self) -> LMC_FileType:
        return self._filetype

    # Creates a generator from the file, yielding each line in the file. 
    def lines(self):
        with self._path.open() as f:
            yield from f


