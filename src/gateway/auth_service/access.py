import os, requests

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("Missing credentials", 401)

    basicAuth = requests.auth.HTTPBasicAuth(auth.username, auth.password)

    res = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDR')}/login",
        auth=basicAuth
    )
    if res.status_code == 200:
        return res.txt, None
    else:
        return None, (res.text, res.status_code)
    