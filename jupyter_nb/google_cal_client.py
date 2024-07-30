import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalClient:
    """For reading and writing Google calendar entries via the Google calendar API."""

    def __init__(self):
        # If modifying these scopes, delete the file token.json.
        self.SCOPES = ["https://www.googleapis.com/auth/calendar"]
        
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

    def create_event(self, event_details):
        event = {
            'summary': event_details["description"],
            'colorId': '4',
            'description': 'This event generated automatically from the Waldis toggl gateway script.',
            'start': {
                'dateTime':  event_details["start"],
            },
            'end': {
                'dateTime':  event_details["stop"],
            },
        }
        try:
            service = build("calendar", "v3", credentials=self.creds)

            event = service.events().insert(calendarId='primary', body=event).execute()
            print ('Event created: %s' % (event.get('htmlLink')))

        except HttpError as error:
            print(f"An error occurred: {error}")
