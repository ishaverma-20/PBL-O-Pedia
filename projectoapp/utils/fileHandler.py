import logging

logger = logging.getLogger(__name__)


class FileHandler:
    def __init__(self, filePath):
        self.filePath = filePath
        self.fh = None

    def start(self, mode):
        if not self.fh:
            self.fh = open(self.filePath, mode)
            logger.info('Opend the file: %s', self.filePath)
        else:
            logger.info('File %s is already opened', self.filePath)

    def close(self):
        if self.fh:
            logger.info('Closing the file %s', self.filePath)
            self.fh.close()
            self.fh=None

    def exist(self):

        pass


class TxtFileHandler(FileHandler):
    def __init__(self, filePath):
        super().__init__(filePath)

    def start(self, mode):
        super().start(f'{mode}t')

    def writeLine(self,textLine):
        self.fh.write(f"\n{textLine}")

    def writeLines(self,textLines):
        self.fh.writelines(textLines)

    def readLine(self) -> str:
        return self.fh.readline()


