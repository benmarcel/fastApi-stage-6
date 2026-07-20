from fastapi_mail import ConnectionConfig
from middlewares.utilities import get_env_variable
from pydantic import SecretStr
conf = ConnectionConfig(
    MAIL_USERNAME=get_env_variable("MAIL_USERNAME"),
    MAIL_PASSWORD=SecretStr(get_env_variable("MAIL_PASSWORD")),
    MAIL_FROM=get_env_variable("MAIL_FROM"),
    MAIL_PORT=int(get_env_variable("MAIL_PORT")),
    MAIL_SERVER=get_env_variable("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)