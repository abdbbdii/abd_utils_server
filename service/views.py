import os
import requests

from django.http import JsonResponse
from django.shortcuts import redirect


def this(request):
    r = {
        "scheme": request.scheme,
        "path": request.path,
        "absolute_uri": request.build_absolute_uri(),
        "content_type": request.content_type,
        "content_params": request.content_params,
        "encoding": request.encoding,
        "path_info": request.path_info,
        "session": request.session.session_key,
        # "session_data": {k: request.session[k] for k in request.session.keys()},
        "COOKIES": request.COOKIES,
        "method": request.method,
        "GET": request.GET,
        "POST": request.POST,
        "FILES": request.FILES,
        "data": request.body.decode("utf-8"),
    }
    print(r)
    return JsonResponse(r)


def trigger_workflow(request):
    """
    - Trigger a GitHub workflow using the GitHub API.
    - Example: http://localhost:8000/service/trigger-workflow?owner=abdbbdii&repo=abdbbdii&event=update-readme&redirect_uri=http://github.com/abdbbdii/abdbbdii
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
