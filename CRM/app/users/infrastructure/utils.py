import requests


def verify_recaptcha(recaptcha_response):
    RECAPTCHA_SECRET_KEY = 'your_recaptcha_secret_key'  # noqa
    # Make a POST request to the Google reCAPTCHA API to verify the response
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
    )
    # Parse the response and check if reCAPTCHA verification succeeded
    if response.status_code == 200:
        data = response.json()
        return data.get('success', False)
    return False
