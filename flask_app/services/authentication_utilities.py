import firebase_admin
from firebase_admin import auth, credentials
from constants.general_constants import Files


def firebase_setup():
    """
    Initialize app with firebase
    """
    cred = credentials.Certificate(Files.FIREBASE_ADMIN_SDK_CREDENTIALS)
    firebase_admin.initialize_app(cred)


def get_user_uid(id_token):
    """
    Get user uid from id_token returned from Firebase Admin SDK
    :param id_token: (string) id_token from client-side returned by firebase
    :return: (string) user uid stored by Firebase
    """
    
    decoded_token = auth.verify_id_token(id_token)
    return decoded_token["uid"]
