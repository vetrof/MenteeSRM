import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())


    try:
        service = build("calendar", "v3", credentials=creds)

        # Calculate the date 7 days from now
        now = datetime.datetime.utcnow()
        future_date = now + datetime.timedelta(days=7)
        future_date_iso = future_date.isoformat() + "Z"  # 'Z' indicates UTC time

        # Call the Calendar API with the future date
        print("Getting the upcoming 10 events for the next 7 days")
        events_result = (
            service.events()
            .list(
                calendarId="snotaf716h667sj4fn8ac67kg4@group.calendar.google.com",
                timeMin=now.isoformat() + "Z",
                timeMax=future_date_iso,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Create a list of dictionaries to store event details
        events_list = []

        # Append the start and summary of each event to the list
        for event in events:
            # start = event["start"].get("dateTime", event["start"].get("date"))
            start = event["start"]
            events_list.append({"start": start, "summary": event["summary"]})

        # print(events_list)
        return events_list

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
