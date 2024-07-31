# Copy toggl time entries to Google calendar

A Zapier replacement that copies "toggl" (https://toggl.com) time entries to Google calendar using their respective APIs.

## Directory Structure

### jupyter_nb
Contains a jupyter notebook that copies the last toggl time entry to Google calendar.  Used only for development, testing and debugging.  Requires the user to trigger the copy.

### gcloud_function
The files that run in the Google cloud.  Triggered via a webhook initiated from toggl whenever a time entry is updated.  The copy happens automatically, no user intervention is required.
