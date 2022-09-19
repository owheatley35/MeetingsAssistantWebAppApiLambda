import json

from jose import jwt

from data.provider.UserRoleProvider import UserRoleProvider
from roles.User import User
from security.credentials import auth0_domain, api_audience, algorithms, auth0_key
from security.exceptions.AuthError import AuthError
from six.moves.urllib.request import urlopen
import urllib.request as url_request


# Gather configuration information from credentials.py
AUTH0_DOMAIN = auth0_domain
API_AUDIENCE = api_audience
ALGORITHMS = algorithms
AUTH0_KEY = auth0_key


def get_public_signing_key():
    """
    Retrieves the public signing key from Auth0.
    """
    f = url_request.urlopen(AUTH0_KEY)
    key = f.read()
    return key


class UserAuthorizer:
    """
    Class to authorise a user based on the JWT provided in the header.
    """

    def __init__(self, header):
        """
        Constructor for the UserAuthorizer class.
        :param header: The header from the request.
        """
        self._header = header

    def _get_token_auth_header(self):
        """
        Obtains the Access Token from the Authorization Header
        """
        auth = self._header.get("Authorization", None)
        if not auth:
            raise AuthError({"code": "authorization_header_missing",
                             "description":
                                 "Authorization header is expected"}, 401)

        parts = auth.split()

        if parts[0].lower() != "bearer":
            raise AuthError({"code": "invalid_header",
                             "description":
                                 "Authorization header must start with"
                                 " Bearer"}, 401)
        elif len(parts) == 1:
            raise AuthError({"code": "invalid_header",
                             "description": "Token not found"}, 401)
        elif len(parts) > 2:
            raise AuthError({"code": "invalid_header",
                             "description":
                                 "Authorization header must be"
                                 " Bearer token"}, 401)

        token = parts[1]
        return token

    def authorise_user(self) -> User:
        """
        Determines if the Access Token is valid
        """
        token = self._get_token_auth_header()
        jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://" + AUTH0_DOMAIN + "/"
                )

            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                 "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                 "description":
                                     "incorrect claims,"
                                     "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                 "description":
                                     "Unable to parse authentication"
                                     " token."}, 401)

            current_user = payload

            try:
                user_id = str(payload.get("sub"))
                current_user_id = user_id.split('|')[1]
            except Exception:
                raise AuthError({"code": "missing_user_id",
                                 "description":
                                     "Unable to find user id"
                                     " token."}, 401)

            user_role = self.retrieveUserRole(current_user_id)

            return User(current_user_id, user_role)

        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 401)

    def retrieveUserRole(self, user_id: str) -> str:
        retrieve_rows = UserRoleProvider(user_id)
        return retrieve_rows.get_user_role()
