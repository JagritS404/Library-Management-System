from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from config import settings


oauth = OAuth()
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'


oauth.register(
name='google',
client_id=settings.GOOGLE_CLIENT_ID,
client_secret=settings.GOOGLE_CLIENT_SECRET,
server_metadata_url=CONF_URL,
client_kwargs={'scope': 'openid email profile'},
)


async def google_login(request: Request):
redirect_uri = request.url_for('auth:google_callback')
return await oauth.google.authorize_redirect(request, redirect_uri)


async def google_callback(request: Request):
token = await oauth.google.authorize_access_token(request)
user = await oauth.google.parse_id_token(request, token)
return user