'''
This class handles DATA API requests to a FileMaker server.
v1 of the DATA API is a feature of FileMaker Server 17 (this class is not compatible with FileMaker Server 16 or earlier)
Special Thanks to Andrew Wolfe for the initial build of this class.
'''

import requests, json
from requests.auth import HTTPBasicAuth
import urllib3

class DataAPIv1:

    def __init__(self, server, secure=True):
        self._api_url = 'https://' + server + '/fmi/data/v1/databases'
        self._return_data = []
        self.errorCode = 0
        self.errorMessage = 'OK'
        self._api_key = None
        self.solution = None
        self.secure = secure

        if not self.secure:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def authenticate(self, solution, username, password):
        self.solution = solution
        auth = HTTPBasicAuth(username,password)
        data = {'fmDataSource': [{"database": self.solution}]}
        req = self._request('auth', 'post', data=data, auth=auth)

        if req['messages'][0]['code'] != "0":
            print("Error")
        else:
            self._api_key = req['response']['token']

        return req

    def logout(self):
        '''Log out of the current session in a filmaker solution'''
        req = self._request('auth', 'delete')
        self._api_key = None
        self.solution = None
        return req

    def get_records(self, layout, args={}):
        my_range = 100
        # adding a recursive function to handle paging with the range limit set at 100
        self._page_recursive(layout, my_range, 1)
        return self._build_custom_response(data=self._return_data)

    def get_record(self, layout, record_id, args={}):
        # get a single record by it's record ID
        return self._request('record', 'get', layout, record_id=record_id, query_params=args)

    def create_record(self, layout, data):
        '''create a new record in the specified layout'''
        return self._request('record', 'post', layout, data=data)

    def delete_record(self, layout, record_id):
        return self._request('record', 'delete', layout, record_id=record_id)

    def find_records(self, layout, data):
        # query must be in the form of JSON data
        # eg: {query: [ { "Company" : "*Hospital", "Group": "=Nurse"}]}
        return self._request('find', 'post', layout, data=data)

    def edit_record(self, layout, record_id, data):
        '''Update a record for a recordId in the specified layout.'''
        return self._request('record', 'patch', layout, record_id=record_id, data=data)

    def set_globals(self, data):
        '''Set a global fields in a solution; doesn't need layout context'''
        return self._request('globals', 'patch', data=data)

    def container_upload(self, layout, record_id, field_name, file, field_repetition=1):
        url = str(field_name) + "/" + str(field_repetition)
        return self._request('container', 'post', layout, record_id=record_id, containerURL=url, file=file)

    def _page_recursive(self, layout, my_range, offset):
        args = {}
        args['_limit'] = str(my_range)
        args['_offset'] =  str(offset)
        response = self._request('record', 'get', layout, query_params=args)
        if self.errorCode != 0:
            print("Error getting records, code: " + str(self.errorCode) + ', Message: ' +
                    self.errorMessage + "\n")
        data_one = response['response']['data']
        for item in data_one:
            self._return_data.append(item)
        count = len(response['response']['data'])
        if count == my_range:
            # there are probably more records do another request to see
            # add current offset to range to get the new offset value
            self._page_recursive(layout, my_range, offset + my_range)
        else:
            # when count no longer equals range we know we have reached the end so exit
            # function
            return

    def _build_custom_response(self, data=None):
        response = {'response': {},
                    'messages': [
                        {'code': str(self.errorCode),
                         'message': self.errorMessage}
                    ]
                    }

        if data:
            response['response']['data'] = data

        return response

    def _request(self, method, verb, layout='', record_id='', query_params={}, data=None, auth=None, containerURL='', file=''):
        """ Makes a Filemaker API call and returns the response as an array."""

        if not self.solution:
            self.errorCode = -1
            self.errorMessage = "Solution name missing. Please re-authenticate."
            return self._build_custom_response()

        # build the header
        if method == "auth" and verb == "post":
            # we're loggin into the solution
            headers = {"Content-Type": "application/json"}
        else:
            if method == "container":
                headers = {"Authorization": "Bearer " + self._api_key}
            elif verb == 'patch' or verb == 'post':
                headers = {"Authorization": "Bearer " + self._api_key, "Content-Type": "application/json"}
            else:
                headers = {"Authorization": "Bearer " + self._api_key}

        if method == "container":
            data_json = data
        else:
            data_json = json.dumps(data)

        # build the url
        if method == 'auth':
            url = self._api_url + "/" + self.solution + "/sessions"
            if verb == 'delete':
                url += "/" + self._api_key
        elif method == 'globals':
            url = self._api_url + "/" + self.solution + "/globals"
        elif method == 'find':
            url = self._api_url + "/" + self.solution + "/layouts/" + layout + "/_find"
        else:
            url = self._api_url + "/" + self.solution + "/layouts/" + layout + "/records"
            if record_id != '':
                # needed for delete record, edit record, and get record
                url += "/" + record_id
            if containerURL != '':
                # needed for uploading into container fields
                url += "/containers/" + containerURL

        self.data_sent = data_json
        self.url = url

        test_url = 'https://webhook.site/b540812c-f488-482e-a153-d22e8c6fddb4'

        try:
            req = ''
            # complete the request
            if verb == "get":
                req = requests.get(url, headers=headers, params=query_params,
                                   verify=self.secure)
            elif verb == "post":
                if auth:
                    req = requests.post(url, data=data_json, headers=headers, auth=auth, verify=self.secure)
                elif method == "container":
                    req = requests.post(url, files={'upload': file}, headers=headers, verify=self.secure)
                else:
                    req = requests.post(url, data=data_json, headers=headers,
                                        verify=self.secure)
            elif verb == "patch":
                req = requests.patch(url, data=data_json, headers=headers,
                                     verify=self.secure)
            elif verb == "delete":
                req = requests.delete(url, headers=headers, verify=self.secure)
        except Exception as e:
            self.errorCode = -3
            self.errorMessage = "Could not connect to server: " + str(req) + "\n" + str(e)
            return self._build_custom_response()

        try:
            req = req.json()
            self.errorCode = int(req['messages'][0]['code'])
            self.errorMessage = req['messages'][0]['message']
            return req
        except json.decoder.JSONDecodeError:
            self.errorCode = -2
            self.errorMessage = "Unexpected response from server: " + str(req)
            return self._build_custom_response()
