# General Constants
STRING_SPLITTER: str = "/#&-"
STRING_DATE_SPLITTER: str = '-'
STRING_TIME_SPLITTER: str = ':'
BETA_NAME: str = "BETA"
PROD_NAME: str = "PROD"

# Security
ADMIN_ROLE_NAME: str = "role:admin"
ALLOWED_ORIGINS = {
    "BETA": "https://d39fabdbkbjoyk.cloudfront.net",
    "PROD": "https://d2v87sbys8bkb2.cloudfront.net"
}

# Configuration
REGION: str = "eu-west-2"
SECRETS_CLIENT_NAME: str = "secretsmanager"
