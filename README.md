# filemakerAPI

###### A python helper library to interact with the FileMaker Data API

This module is compatible with FileMaker Server 17 which uses version 1 of the FileMaker Data API. It includes a paging function that automatically limits the number of records returned from FileMaker within a single API call. It also makes it much easier to manage the tokenization required by the FileMaker API, allowing you to focus on the requests to create or get records from FileMaker.

If enough people are interested, this library can be expanded to also include the Admin API.

## Getting Started

### Installation

fmrest can be installed using pip, or by downloading the source code on GitHub.

```
pip install fmrest
```

## Usage

Initiate an instance of the API with your server name. Do not include “https://“ as this is assumed by the script and required by FileMaker Server.

```
from filemakerAPI import dataAPI

fm = dataAPI.DataAPIv1('filemaker.company.com')
```

To authenticate, pass your solution name, username, and password as a string to the `authenticate` method.

```
fm.authenticate('solutionName', 'username', 'password')
if fm.errorCode != 0:
    print(fm.errorMessage)
```

As shown, you can always check the errorCode and errorMessage attributes to get the last error code given by your FileMaker server.

At the end of your script, run the `logout` method to ensure that no future requests can be made with your API token. This will also close the API's session within FileMaker server.

```
fm.logout()
```

## Interacting with Data

The rest of the methods are fairly self-explanatory. Refer the the API documentation on your FileMaker server for the corresponding JSON data you’ll need to pass to the helper file.

Use standard python dictionaries to build the JSON data and it will be properly converted to a JSON string before being sent to FileMaker.

When this guide references a “Record ID”, keep in mind this is FileMaker’s internal ID for the record, not the primary key in your table. When you pull the data out of FileMaker using a Get Records or Find Records command, this internal ID will be passed back to you. It can also be retrieved using the `Get ( RecordID )` calculation of FileMaker.

**Create a new record:**
```
data = {
    "fieldData": {
        "First Name": "Joe",
        "field2": "More text"
    }
}
fm.create_record('layoutName', data)
```

**Delete a Record**
```
fm.delete_record('layoutName', 'recordId')
```

**Edit a Record**
```
data = {
    "fieldData": {
        "First Name": "Joe",
        "field2": "More text"
    }
}

fm.edit\_record('layoutName', 'recordId', data)
```

**Set Global Field(s)**
```
data = { "globalFields": {
    "tableName1::globalFieldName1":"globalFieldValue1",
    "tableName2::globalFieldName2":"globalFieldValue2"
    }
}
fm.set_globals(data)
```

**Get all records from a layout:**
```
fm.get_records('layoutName')
```

**Get a single record from a layout**
```
fm.get_record('layoutName', 'recordId')
```

**Upload to a Container Field**

Not yet tested

**Find Records**
```
data = {
 "query”:[ {"Group": "=Surgeon", "Work State" : "CA"}, {"Group": "=Surgeon", "Work State" : "NY"}],
 "sort":[ { "fieldName": "Work State", "sortOrder": "ascend" }, { "fieldName": "FirstName", "sortOrder": "ascend" } ]
}
fm.find_records('layoutName', data)
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

