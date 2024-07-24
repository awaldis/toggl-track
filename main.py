import functions_framework
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'payload' in request_json:
        if 'description' in request_json['payload']:
            description = request_json['payload']['description']
        else:
            description = '!! No description found !!'
                
        if 'start' in request_json['payload']:
            start = request_json['payload']['start']
        else:
            start = '!! No start time found !!'

        print(f'Description: {description} - Start time: {start}')

    print('request_json = {}'.format(request_json))

    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json', 
        scopes=['https://www.googleapis.com/auth/calendar']
    )

    event = {
        'summary': 'Test Google Cloud Function',
        'colorId': '4',
        'description': 'This event generated automatically from the Waldis toggl gateway script.',
        'start': {
            'dateTime':  '2024-07-24T18:00:00+00:00',
        },
        'end': {
            'dateTime':  '2024-07-24T19:00:00+00:00',
        },
    }
    try:
        service = build("calendar", "v3", credentials=credentials)

        calendarId=os.environ["CALENDAR_EMAIL"]
        print(f"Using calendarID: {calendarId}")

        event = service.events().insert(calendarId=calendarId, body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print(f"An error occurred: {error}")

    if request_json and 'name' in request_json:
        name = request_json['name']
        print('request_json name field:{}'.format(name))
    elif request_args and 'name' in request_args:
        name = request_args['name']
        print('request_args name field:{}'.format(name))
    else:
        name = 'World2'
        print('No name field found.')
    return 'Hello {}!'.format(name)
