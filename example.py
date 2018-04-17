
import fmDataAPI

fm = fmDataAPI.DataAPIv1('filemaker.company.com')

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

# you must get the record ID from a previous response from the FileMaker server.
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

fm.logout('solutionName')
