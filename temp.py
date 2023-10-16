from googleapiclient import 
# calendar

calendar = service.calendars().get(calendarId='primary').execute()

print calendar['summary']