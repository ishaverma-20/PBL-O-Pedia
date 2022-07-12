from django.contrib import auth
import enum

class ProjectStatus(enum.Enum):
    
    NotStarted=0
    InProgress=1
    Completed=2
    Suspended=3

class BaseModel:
    fieldSepartor='|' # pipe based separation of project when used for representation of all fields
    fieldList=None
    def get_id(self)->str:
        pass
    def set_id(self,id)->str:
        pass
    def get_dictObj(self):
        dictObj ={}
        for field in self.fieldList:
            fldObj = getattr(self,field)
            dictObj[field] = fldObj.value if  isinstance(fldObj,enum.Enum) else fldObj
        return dictObj
    
class Project(BaseModel):
    """Information about the project being maintained by institution"""
    
    fieldList=['id','name','domain','div','coordinatior_id','status']

    def __init__(self,fieldDict) -> None:
        super().__init__()
        self.name = fieldDict['name']
        self.id=fieldDict['id']
        self.domain= fieldDict['domain']
        self.coordinatior_id=fieldDict['coordinatior_id']        
        self.status=ProjectStatus(int(fieldDict['status']))
        self.div=fieldDict['div']
 
    def get_Id(self)->str:
        return self.id

    def __str__(self):
        return self.name

class ProjectReview(BaseModel):
    """Review infroamtion for the projects maintained by institution"""

    fieldList=['id','project_id','rating','user_name','creation_date','review_com']
    
    def __init__(self,fieldDict) -> None:
        super().__init__()
        self.id=fieldDict['id']
        self.project_id= fieldDict['project_id']
        self.rating=fieldDict['rating']        
        self.review_com=fieldDict['review_com']
        self.creation_date=fieldDict['creation_date']
        self.user_name=fieldDict['user_name']
 
    def get_Id(self)->str:
        return self.id
    
    def set_id(self,id)->str:
        self.id = id
    
    def __str__(self):
        return self.id

class Student(BaseModel):
    """Information about the strudent in the institution"""

    fieldList=['id','name','project_id','address','date_of_birth','mail']
    def __init__(self,fieldDict) -> None:
        super().__init__()
        self.name = fieldDict['name']
        self.id=fieldDict['id']
        self.project_id= fieldDict['project_id']
        self.address=fieldDict['address']
        self.date_of_birth=fieldDict['date_of_birth']
        self.mail=fieldDict['mail']
    
    def get_Id(self)->str:
        return self.id
    
    def __str__(self):
        return self.name

    

class Employee(BaseModel):

    """Information about the employee in the institution"""

    fieldList=['id','name','address','date_of_birth','mail','designation']
       
    def __init__(self,fieldDict) -> None:
        super().__init__()
        self.name = fieldDict['name']
        self.id=fieldDict['id']
        self.address=fieldDict['address']
        self.date_of_birth=fieldDict['date_of_birth']
        self.mail=fieldDict['mail']
        self.designation=fieldDict['designation']
    
    def get_Id(self)->str:
        return self.id
    
    def __str__(self):
        return self.initialled_name()


class Contact(BaseModel):
    """Information about the contacts"""

    fieldList=['id','name','rollno','email',]
    def __init__(self,fieldDict) -> None:
        super().__init__()
        self.name = fieldDict['name']
        self.id=fieldDict['id']
        self.rollno= fieldDict['rollno']
        self.email=fieldDict['email']
    
    def get_Id(self)->str:
        return self.id
    
    def __str__(self):
        return self.name