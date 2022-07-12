from http.client import HTTPException
from lib2to3.pytree import Base

from projectoapp.exceptions import ProjectoException
from .utils.parsers import CSVParser, CSVVWriter
from .models import BaseModel

class ModelMgr:
    def __init__():
        pass

    def all(self):
        pass
    def add(self, modelObj):
        pass
    def delete(self, modelObj):
        pass
    def update(self, modelObj):
        pass
    def get(self, id):
        pass
    def refresh(self):
        pass

class FileModelMgr(ModelMgr):
    
    def __init__(self, modelClass,filePath):
        self.filePath = filePath
        self.modelCls = modelClass
        self.csvParser = CSVParser(filePath,modelClass.fieldSepartor,modelClass.fieldList)
        self.modelsDict = {}
        self.csvWriter = CSVVWriter(filePath,modelClass.fieldSepartor,modelClass.fieldList)
        self.nextId=None
        
    
    def load(self)->dict[str:BaseModel]:
        if not len(self.modelsDict):
            self.__laodModelObjects_()
        return self.modelsDict
    
    def all(self)->dict[str:BaseModel]:
        if not len(self.modelsDict):
            raise ProjectoException("Model manager Not initialized properly")
        return self.modelsDict
           
    def refresh(self)->None:
        self.modelsDict.clear()
        self.__laodModelObjects_()

    def __laodModelObjects_(self):

        if not len(self.modelsDict):
            self.csvParser.start(None)
            while fieldList := self.csvParser.next_rec():
                modelObj = self.modelCls(fieldList)
                self.modelsDict[modelObj.get_Id()] = modelObj
            self.nextId = modelObj.get_Id()
            self.csvParser.close()
    
    def add(self, modelObj):
        if self.nextId.isdigit():
            self.nextId = str(int(self.nextId) + 1)
        modelObj.set_id(self.nextId)
        self.csvWriter.addRec(modelObj)
        self.modelsDict[modelObj.get_Id()] = modelObj

    def delete(self, modelObj):
        pass
    def update(self, modelObj):
        if not self.modelsDict.get(modelObj.get_Id()):
            raise HTTPException(f"Object {self.modelCls} with id {modelObj.modelObj.get_Id()} doesn't exist")
        self.modelsDict[modelObj.get_Id()] = modelObj
        self.csvWriter.writeRecords(self.modelsDict.values())
        
    def get(self, id):
        return self.modelsDict.get(id)