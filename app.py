""""Main setup module for Flask App"""
import os

from api import create_app


app = create_app(os.getenv('FLASK_ENV'))


if __name__ == '__main__':
    app.run('0.0.0.0', os.getenv('PORT', 5001))
