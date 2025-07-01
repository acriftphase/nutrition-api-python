"""
Avocavo Nutrition API Python SDK
Fast, accurate nutrition data with USDA verification
"""

from .client import NutritionAPI, ApiError
from .auth import login, logout, get_current_user
from .models import (
    Nutrition, 
    USDAMatch, 
    IngredientResult, 
    RecipeResult, 
    BatchResult,
    Account,
    Usage
)

# Version
__version__ = "1.0.3"
__author__ = "Avocavo"
__email__ = "support@avocavo.com"
__description__ = "Python SDK for the Avocavo Nutrition API"

# Quick access functions
from .client import analyze_ingredient, analyze_recipe

__all__ = [
    # Main client
    'NutritionAPI',
    'ApiError',
    
    # Authentication
    'login',
    'logout', 
    'get_current_user',
    
    # Data models
    'Nutrition',
    'USDAMatch',
    'IngredientResult',
    'RecipeResult', 
    'BatchResult',
    'Account',
    'Usage',
    
    # Quick functions
    'analyze_ingredient',
    'analyze_recipe',
    
    # API key management (when using NutritionAPI client)
    # Access via: client.list_api_keys(), client.create_api_key(), etc.
    
    # Package info
    '__version__',
    '__author__',
    '__email__',
    '__description__'
]