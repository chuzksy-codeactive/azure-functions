import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL = "chuzksy-server-pg.postgres.database.azure.com"  # TODO: Update value
    POSTGRES_USER = "azureuser@chuzksy-server-pg"  # TODO: Update value
    POSTGRES_PW="Password001001"   #TODO: Update value
    POSTGRES_DB = "techconfdb"  # TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING = 'Endpoint=sb://chuzkys-notification.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=Aez7ht1986ad8WR2OAyIo2xysneqocBNXx7beJ0i2pc='  # TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'info@techconf.com'
    SENDGRID_API_KEY = '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'  # Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False