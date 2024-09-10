import json
import requests


def sign_in_with_email_and_password(api_key, email, password):
    """
    Firebaseで認証を行う(SDKの signInWithEmailAndPassword と同値)

    :param api_key:
    :param email:
    :param password:
    :return: Firebaseの、idTokenなどを含んだ、認証情報
    """
    # https://firebase.google.com/docs/reference/rest/auth/#section-sign-in-email-password
    uri = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={api_key}"
    headers = {"Content-type": "application/json"}
    data = json.dumps({"email": email, "password": password,
                      "returnSecureToken": True})

    result = requests.post(url=uri,
                           headers=headers,
                           data=data)
    return result.json()
