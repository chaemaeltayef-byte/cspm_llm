# This simulates receiving data from your colleague's AI model.
# Later, replace the fake_threats list with a real API call or shared file.

def get_threats_from_model() -> list:
    """
    In production: call your colleague's model endpoint here.
    For now: returns fake threat data so you can test independently.
    """
    fake_threats = [
        {"threat": "UnauthorizedRootAccess", "score": 0.94},
        {"threat": "OpenS3BucketExposed",    "score": 0.88},
        {"threat": "WeakIAMPolicy",          "score": 0.76},
    ]
    return fake_threats

# When your colleague is ready, replace with something like:
# import requests
# def get_threats_from_model():
#     response = requests.get("http://colleague-api/threats")
#     return response.json()