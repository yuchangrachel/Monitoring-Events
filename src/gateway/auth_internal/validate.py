import os, requests

def validate(request):
    if not 'Authorization' in request.headers:
        return "Missing credentials", 401
    
    token = request.headers["Authorization"]

    if not token:
        return None, ("Missing credentials", 401)

    res = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDR')}/validate",
        headers={"Authorization": token}
    )
    if res.status_code == 200:
        return res.text, None
    else:
        return None, (res.text, res.status_code)