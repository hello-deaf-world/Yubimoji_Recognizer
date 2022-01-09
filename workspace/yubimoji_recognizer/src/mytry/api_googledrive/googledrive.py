import inspect
import os
import sys
PYPATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/"
# ROOTPATH = PYPATH + "."
# sys.path.append(ROOTPATH)
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

def main():
    creds = None
    if os.path.exists("{}token.json".format(PYPATH)):
        creds = Credentials.from_authorized_user_file("{}token.json".format(PYPATH), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "{}secrets/credentials/test20211024_moheji_desktop.json".format(PYPATH), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("{}token.json".format(PYPATH), "w") as token:
            token.write(creds.to_json())

    service = build("drive", "v3", credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get("files", [])

    if not items:
        print("No files found.")
    else:
        print("Files:")
        for item in items:
            print(u"{0} ({1})".format(item["name"], item["id"]))

if __name__ == "__main__":
    main()