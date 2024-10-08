import pickle
import base64
import json

import google.auth.exceptions
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from .appSettings import appSettings


def authenticate(scopes, token=None):
    """
    Authenticates the user using OAuth2 credentials and returns the credentials object.
    """

    if not appSettings.google_credentials:
        raise ValueError("Google credentials not found in the database.")

    print("Checking stored credentials...")
    creds = None

    if token:
        try:
            creds = pickle.loads(base64.b64decode(token))
        except Exception as e:
            print(f"Failed to load credentials: {e}")
            creds = None

    if creds and creds.valid:
        return token

    elif creds and creds.expired and creds.refresh_token:
        try:
            print("Refreshing access token...")
            creds.refresh(Request())
            print("Token refreshed successfully.")
        except google.auth.exceptions.RefreshError:
            print("Token refresh failed. Starting new authentication flow...")
            creds = None

    if not creds or not creds.valid:
        print("Authenticating with Google...")
        flow = InstalledAppFlow.from_client_config(json.loads(appSettings.google_credentials), scopes)
        creds = flow.run_local_server(port=0)

        print("Authenticated and token stored successfully.")
        print(base64.b64encode(pickle.dumps(creds)).decode("utf-8"))

    return base64.b64encode(pickle.dumps(creds)).decode("utf-8")
