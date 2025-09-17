"""
Azure Web App startup file
This file is used by Azure to start the Flask application
"""

import os
import sys

# Add the application directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    app.run()