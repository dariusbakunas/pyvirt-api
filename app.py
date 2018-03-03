# coding=utf-8
import os
from pyvirt import create_app

config_name = os.getenv('FLASK_CONFIGURATION', 'development')
app = create_app(config_name)
app.logger.info(config_name)

if __name__ == '__main__':
    app.run()
