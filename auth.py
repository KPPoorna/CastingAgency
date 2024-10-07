import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

auth0_domain = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = ['RS256']
api_audience = os.getenv('API_AUDIENCE')

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
    This method returns the token part of the header
    It attempts to get the header from the request 
        and if no header is present, raises an AuthError 
    It attempts to split bearer and the token
        and raises an AuthError if the header is malformed
    
'''
def get_token_auth_header():
    auth = request.headers.get('Authorization',None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split() 

    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must have a Bearer at the start.'
        }, 401)
    
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found in authorization header.'
        }, 401)
    
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must just have a Bearer and a token.'
        }, 401)
    
    token = parts[1]
    
    return token
    

'''
    @INPUTS
        permission: string permission (i.e. 'post:actor')
        payload: decoded jwt payload

    This method raises an AuthError if permissions are not included in the payload
    It raises an AuthError if the requested permission string is not in the payload permissions array
    Returns true otherwise
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 403)
    
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found in JWT.'
        }, 403)
    
    return True


'''
    @INPUTS
        token: a json web token (string)
        The token is an Auth0 token with key id (kid)
    This method verifies the token using Auth0 /.well-known/jwks.json
    It decodes the payload from the token and validates the claims
    finally returns the decoded payload

'''
def verify_decode_jwt(token):
    jwks_url = f'https://{auth0_domain}/.well-known/jwks.json'
    response = requests.get(jwks_url)
    jwks = response.json()

    # Get the key ID from the token header
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=api_audience,
                issuer='https://' + auth0_domain + '/'
            )

            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

'''
Implementation of @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    This method uses the get_token_auth_header method to get the token
    it uses the verify_decode_jwt method to decode the jwt
    it uses the check_permissions method, validate claims and checks the requested permission
    returns the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator