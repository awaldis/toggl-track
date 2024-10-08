import functions_framework
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

@functions_framework.http
def toggl_time_entry_webhook_http(request):
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

    # Parse out the description and start and stop times OR
    # return with an error message if they can't be found.
    if request_json and 'payload' in request_json:
        if 'description' in request_json['payload']:
            description = request_json['payload']['description']
        else:
            description = '!! No description found !!'
            return description
                
        if 'start' in request_json['payload']:
            start = request_json['payload']['start']
        else:
            start = '!! No start time found !!'
            return start

        if 'stop' in request_json['payload']:
            stop = request_json['payload']['stop']
        else:
            stop = '!! No stop time found !!'
            return stop

        print(f'Description: {description} - Start time: {start} - Stop time: {stop}')
    else:
        return 'No payload field found!'

    # If we get to this point then the description, start and stop times
    # must have been found and we can proceed to creating the event on the Google
    # calendar.

    print('request_json = {}'.format(request_json))

    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json', 
        scopes=['https://www.googleapis.com/auth/calendar']
    )

    event = {
        'summary': description,
        'colorId': '4',
        'description': 'This event generated automatically from the Waldis toggl gateway script.',
        'start': {
            'dateTime':  start,
        },
        'end': {
            'dateTime':  stop,
        },
    }
    try:
        service = build("calendar", "v3", credentials=credentials)

        calendarId=os.environ["CALENDAR_EMAIL"]

        event = service.events().insert(calendarId=calendarId, body=event).execute()
        print ('Event created: %s' % (event.get('htmlLink')))
        return(f'Event created - Description: {description} - Start time: {start} - Stop time: {stop}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        return(f"An error occurred: {error}")
