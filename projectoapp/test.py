
from django.conf import settings
dirObj={}
dirObj['Name'] = 'Isha Verma'
dirObj['Address'] = 'C-203'
print(dirObj['Name'])
print(dirObj['Address'])
listObj = []
listObj.append(dirObj)
print(listObj[0].Name)