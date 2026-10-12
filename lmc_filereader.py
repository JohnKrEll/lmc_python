from enum import Enum


class LMC_FileReader:
    def __init__(self): 
        self._data = list()
        self._filetype = None

    def get_filetype(self):
        return self._filetype

    def get_data(self):
        return self._data

    def from_file(self, filename):
        with open(filename) as file:
            self._data = file.readlines()
        if self._data[0].isnumeric():
            self._filetype = LMC_FileType.MACHINE_CODE
        else:
            self._filetype = LMC_FileType.ASSEMBLY


class LMC_FileType(Enum):
    MACHINE_CODE = 0
    ASSEMBLY = 1
