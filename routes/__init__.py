"""
Make routes directory into package where
Blueprints are imported directly from individual files
"""

from routes.auth import auth
from routes.error import error
from routes.views import views
