import json
import os
import requests

from django.http import JsonResponse
from django.shortcuts import redirect

from .google_authentication import authenticate
from .appSettings import appSettings



def this(request):
    """
    ### Get the request data.
    Path: service/this/
    Method: GET/POST
    """
    r = {
        "scheme": request.scheme,
        "path": request.path,
        "absolute_uri": request.build_absolute_uri(),
        "content_type": request.content_type,
        "content_params": request.content_params,
        "encoding": request.encoding,
        "path_info": request.path_info,
        "session": request.session.session_key,
        "COOKIES": request.COOKIES,
        "method": request.method,
        "GET": request.GET,
        "POST": request.POST,
        "FILES": request.FILES,
        "headers": {k: request.headers[k] for k in request.headers.keys()},
        "data": request.body.decode("utf-8"),
    }
    print(r)
    return JsonResponse(r)


def trigger_workflow(request):
    """
    ### Trigger a GitHub workflow using the GitHub API.
        - Path: service/trigger-workflow/
        - Method: GET
        - Query Parameters:
            - `owner` The owner of the repository.
            - `repo` The repository name.
            - `event` The name of the event to trigger.
            - `redirect_uri` The URL to redirect to after triggering the workflow.
        - http://127.0.0.1:8000/service/trigger-workflow?owner=abdbbdii&repo=abdbbdii&event=update-readme&redirect_uri=http://github.com/abdbbdii/abdbbdii
    """
    REPO_OWNER = request.GET.get("owner", "abdbbdii")
    REPO_NAME = request.GET.get("repo", "abdbbdii")
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
    headers = {"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}", "Accept": "application/vnd.github.everest-preview+json"}
    data = {"event_type": request.GET.get("event", "update-readme")}
    response = requests.post(url, headers=headers, json=data)
    if request.GET.get("redirect_uri"):
        return redirect(request.GET.get("redirect_uri"))
    if response.status_code == 204:
        print("Workflow triggered successfully!")
        return JsonResponse({"message": "Workflow triggered successfully!"})
    else:
        print(f"Failed to trigger workflow: {response.status_code}")
        print(response.text)
        return JsonResponse({"message": "Failed to trigger workflow!", "error": response.text}, status=500)

def google_auth(request):
    try:
        if request.method == 'GET':
            data = json.loads(request.body.decode("utf-8"))
            if data.get("password") != appSettings.password:
                return JsonResponse({"message": "Invalid password."}, status=403)
            try:
                google_creds = authenticate(data.get("scopes"))
                return JsonResponse({"message": "Google authentication successful!", "google_creds": google_creds}, status=200)
            except Exception as e:
                return JsonResponse({"message": str(e)}, status=500)
        else:
            return JsonResponse({"message": "Invalid request."}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e.with_traceback())}, status=400)
