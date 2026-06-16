#!/usr/bin/env python
"""
Run the Flask web application
"""

import os
import sys
from web.app import app
from loguru import logger

if __name__ == '__main__':
    logger.info("Starting Football Prediction Web App...")
    logger.info("Visit http://localhost:5000 in your browser")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )
