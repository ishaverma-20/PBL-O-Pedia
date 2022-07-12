import enum
from xmlrpc.client import boolean
from .fileHandler import TxtFileHandler
import os
import logging

logger = logging.getLogger(__name__)

class CSVParser(TxtFileHandler):
    def __init__(self, filePath, separtor, mdlFieldList):
        super().__init__(filePath)
        self.separtor = separtor
        self.mdlFieldList = mdlFieldList

    def start(self, mode):

        if not mode:
            super().start('r+')
        else:
            super().start(mode)

    def next_rec(self) -> dict[str, str]:
        dictObj=None
        while True:
            if not (rec := super().readLine()):
                return dictObj
            rec = rec.strip()
            # skip the empty line or line which is commented with '#'
            if (not rec) or rec.startswith('#'):
                continue
            valueList = rec.split(self.separtor)
            try:
                dictObj = {self.mdlFieldList[count]: value.strip() for count, value in enumerate(valueList)}
                return dictObj
            except Exception:
                logger.error(f"Error occured while parsing line:{rec}, exception msg:{Exception}")
                continue #continuw with next record
        

class CSVVWriter(TxtFileHandler):
    def __init__(self, filePath, separtor, mdlFieldList):
        super().__init__(filePath)
        self.separtor = separtor
        self.mdlFieldList = mdlFieldList

    # when writing we create temp file to avoid any corruption
    def __start_(self, mode, useTemp=False):
        self.orgPath = None
        if useTemp:
            self.orgPath = self.filePath
            self.filePath = f"{self.filePath}Temp"
        if not mode:
            super().start('a+')
        else:
            super().start(mode)

    def __close_(self): # before clsoing checks if we have to move the file 
        self.close()
        if self.orgPath:# move the file
            os.replace(self.filePath,self.orgPath)
            self.filePath = self.orgPath

    def addRec(self,record)-> boolean:

        if not record:
            return False
        self.__start_('a+')
        self.__writeRec_(self.__getAttrList_(record))
        self.__close_()
        return True

    def __getAttrList_(self,record)->list:
        attrbList = []
        for fieldName  in self.mdlFieldList:
            attrValue= getattr(record,fieldName)
            if type(attrValue) is str:
                attrbList.append(attrValue)
            elif isinstance(attrValue,enum.Enum) :
                attrbList.append(str(attrValue.value))
            else:
                attrbList.append(str(attrValue))
        return attrbList

    def __writeRec_(self,fieldList):
        textLine = self.separtor.join(fieldList)
        self.writeLine(textLine)

    def __writeRecs_(self,fieldLists):
        textLines = [f"{self.separtor.join(fieldList)}\n" for fieldList in fieldLists]
        self.writeLines(textLines)

    def writeRecords(self,records) -> boolean:
        if not records:
            return False
        totlRecords = len(records)
        fieldLists=[]
        self.__start_('w+',True)
        for count, value in enumerate(records, start=1):
            fieldLists.append(self.__getAttrList_(value))
            if count >= 5 or count == totlRecords:
                self.__writeRecs_(fieldLists)
                fieldLists.clear()
        self.__close_()
        return True
