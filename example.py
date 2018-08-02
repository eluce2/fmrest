from fmrest import dataAPI

fm = dataAPI.DataAPIv1('filemaker.company.com')

fm.authenticate('solutionName', 'username', 'password')
if fm.errorCode != 0:
    print(fm.errorMessage)

fm.get_records('layoutName')

data = {
    "fieldData": {
        "First Name": "Joe",
        "field2": "More text"
    }
}
fm.create_record('layoutName', data)

'''
you must get the record ID from a previous response from the FileMaker server
or using the Get(RecordID) function of FileMaker
'''
fm.delete_record('layoutName', 'recordId')

data = {
    "fieldData": {
        "First Name": "Joe",
        "field2": "More text"
    }
}
fm.edit_record('layoutName', 'recordId', data)

fm.get_record('layoutName', 'recordId')

data = {
 "query":[ {"Group": "=Surgeon", "Work State" : "CA"}, {"Group": "=Surgeon", "Work State" : "NY"}],
 "sort":[ { "fieldName": "Work State", "sortOrder": "ascend" }, { "fieldName": "FirstName", "sortOrder": "ascend" } ]
}
fm.find_records('layoutName', data)

data = { "globalFields": {
     "tableName1::globalFieldName1":"globalFieldValue1",
     "tableName2::globalFieldName2":"globalFieldValue2"
     }
}
fm.set_globals(data)

with open('file.png', 'rb') as file:
    fm.container_upload('layoutName', 'recordId', 'container_field_name', file)

fm.logout('solutionName')
