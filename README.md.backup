# 🥑 Avocavo Nutrition API Python SDK

[![PyPI version](https://badge.fury.io/py/avocavo-nutrition.svg)](https://badge.fury.io/py/avocavo-nutrition)
[![Python Support](https://img.shields.io/pypi/pyversions/avocavo-nutrition.svg)](https://pypi.org/project/avocavo-nutrition/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/avocavo-nutrition)](https://pepy.tech/project/avocavo-nutrition)

**The easiest way to get accurate nutrition data for any recipe ingredient.**

Get fast, verified USDA nutrition data with just one line of code. Perfect for recipe apps, fitness trackers, meal planners, and food tech products.

## 🚀 Quick Start

### Installation

```bash
pip install avocavo-nutrition
```

### 🔐 OAuth Login (Recommended)

```python
import avocavo_nutrition as av

# One-time OAuth login (opens browser)
av.login()  # Google OAuth (default)
# av.login(provider="github")  # Or GitHub OAuth

# Now use anywhere in your code without API keys!
result = av.analyze_ingredient("2 cups chocolate chips")
print(f"Calories: {result.nutrition.calories_total}")
print(f"Protein: {result.nutrition.protein_total}g")
print(f"USDA: {result.usda_match.description}")
```

### 🔑 Direct API Key

```python
from avocavo_nutrition import NutritionAPI

client = NutritionAPI(api_key="your_api_key_here")
result = client.analyze_ingredient("1 cup rice")
print(f"Calories: {result.nutrition.calories_total}")
```

## 🎯 What You Can Do

### 🥘 Analyze Ingredients
```python
# Any ingredient with quantity
result = av.analyze_ingredient("2 tbsp olive oil")
if result.success:
    print(f"Calories: {result.nutrition.calories}")
    print(f"Fat: {result.nutrition.fat}g")
    print(f"Verify: {result.verification_url}")
```

### 🍳 Analyze Complete Recipes
```python
# Full recipe with per-serving calculations
recipe = av.analyze_recipe([
    "2 cups all-purpose flour",
    "1 cup whole milk",
    "2 large eggs", 
    "1/4 cup sugar"
], servings=8)

print(f"Per serving: {recipe.nutrition.per_serving.calories} calories")
print(f"Total recipe: {recipe.nutrition.total.calories} calories")
```

### ⚡ Batch Processing (Starter+)
```python
# Analyze multiple ingredients efficiently
batch = av.analyze_batch([
    "1 cup quinoa",
    "2 tbsp olive oil",
    "4 oz salmon",
    "1 cup spinach"
])

for item in batch.results:
    if item.success:
        print(f"{item.ingredient}: {item.nutrition.calories} cal")
```

### 📊 Account Management
```python
# Check your usage and limits
account = av.get_account_usage()
print(f"Plan: {account.plan_name}")
print(f"Usage: {account.usage.current_month}/{account.usage.monthly_limit}")
print(f"Remaining: {account.usage.remaining}")
```

## ✨ Key Features

### 🎯 **USDA Verified Data**
- Real FDC IDs from USDA FoodData Central
- Verification URLs for manual checking
- Prioritized data sources (Foundation > SR Legacy > Survey)

### ⚡ **Lightning Fast**
- **94%+ cache hit rate** = sub-second responses  
- **8,000+ requests/hour** throughput
- Smart caching across all users

### 🧠 **Intelligent Recognition**
- Handles "2 cups flour" or "1 lb chicken breast"
- GPT-powered ingredient matching
- Automatic quantity and measurement parsing

### 🔧 **Developer Friendly**
- Secure credential storage with `keyring`
- Type hints and comprehensive error handling
- Works with environment variables
- Detailed documentation and examples

## 📊 Complete Nutrition Data

```python
result = av.analyze_ingredient("1 cup cooked rice")
nutrition = result.nutrition

# All available nutrients
print(f"Calories: {nutrition.calories}")
print(f"Protein: {nutrition.protein}g")
print(f"Carbs: {nutrition.carbs}g") 
print(f"Fat: {nutrition.fat}g")
print(f"Fiber: {nutrition.fiber}g")
print(f"Sugar: {nutrition.sugar}g")
print(f"Sodium: {nutrition.sodium}mg")
print(f"Calcium: {nutrition.calcium}mg")
print(f"Iron: {nutrition.iron}mg")
```

## 💰 Pricing Plans

| Plan | Monthly Requests | Price | Features |
|------|------------------|-------|----------|
| **Free Trial** | 100 | **Free** | One-time trial credit |
| **Starter** | 2,500 | $9.99/month | Developer dashboard, email support |
| **Pro** | 25,000 | $49/month | Priority support, advanced analytics |
| **Enterprise** | 250,000+ | $249/month | SLA, dedicated support, flexible scaling |

**🎁 No Credit Card Required**: Start with 100 free API calls to test your integration

[**Get your free API key →**](https://nutrition.avocavo.app)

## 🔐 Authentication Options

### Option 1: Login (Recommended)
```python
import avocavo_nutrition as av

# Login once, use everywhere
av.login("user@example.com", "password")

# Credentials stored securely with keyring
result = av.analyze_ingredient("1 cup rice")
```

### Option 2: API Key
```python
from avocavo_nutrition import NutritionAPI

# Direct API key usage
client = NutritionAPI(api_key="your_api_key")
result = client.analyze_ingredient("1 cup rice")
```

### Option 3: Environment Variable
```bash
export AVOCAVO_API_KEY="your_api_key_here"
```

```python
import avocavo_nutrition as av
# API key automatically detected from environment
result = av.analyze_ingredient("1 cup rice")
```

## 🏗️ Real-World Examples

### Recipe App Integration
```python
import avocavo_nutrition as av

def calculate_recipe_nutrition(ingredients, servings=1):
    """Calculate nutrition for any recipe"""
    recipe = av.analyze_recipe(ingredients, servings)
    
    if recipe.success:
        return {
            'calories_per_serving': recipe.nutrition.per_serving.calories,
            'protein_per_serving': recipe.nutrition.per_serving.protein,
            'total_calories': recipe.nutrition.total.calories,
            'usda_verified_ingredients': recipe.usda_matches
        }
    else:
        return {'error': recipe.error}

# Usage
recipe_nutrition = calculate_recipe_nutrition([
    "2 cups flour",
    "1 cup milk", 
    "2 eggs"
], servings=6)
```

### Fitness Tracker Integration  
```python
def track_daily_nutrition(food_entries):
    """Track daily nutrition from food entries"""
    total_nutrition = {
        'calories': 0,
        'protein': 0,
        'carbs': 0,
        'fat': 0
    }
    
    for food in food_entries:
        result = av.analyze_ingredient(food)
        if result.success:
            total_nutrition['calories'] += result.nutrition.calories
            total_nutrition['protein'] += result.nutrition.protein
            total_nutrition['carbs'] += result.nutrition.carbs
            total_nutrition['fat'] += result.nutrition.fat
    
    return total_nutrition

# Usage
daily_foods = [
    "1 cup oatmeal",
    "1 medium banana", 
    "6 oz grilled chicken",
    "2 cups steamed broccoli"
]
daily_totals = track_daily_nutrition(daily_foods)
```

### Restaurant Menu Analysis
```python
def analyze_menu_item(ingredients):
    """Analyze nutrition for restaurant menu items"""
    # Use batch processing for efficiency (Starter+ plans)
    batch = av.analyze_batch(ingredients)
    
    total_calories = sum(
        item.nutrition.calories 
        for item in batch.results 
        if item.success
    )
    
    return {
        'total_calories': total_calories,
        'success_rate': batch.success_rate,
        'ingredients_analyzed': batch.successful_matches
    }
```

## 🛠️ Advanced Usage

### Error Handling
```python
from avocavo_nutrition import ApiError, RateLimitError, AuthenticationError

try:
    result = av.analyze_ingredient("mystery ingredient")
    if result.success:
        print(f"Found: {result.usda_match.description}")
    else:
        print(f"No match: {result.error}")
        
except RateLimitError as e:
    print(f"Rate limit exceeded. Limit: {e.limit}, Usage: {e.usage}")
except AuthenticationError as e:
    print(f"Auth error: {e.message}")
except ApiError as e:
    print(f"API Error: {e.message}")
```

### Configuration
```python
# Use development environment
client = NutritionAPI(
    api_key="your_key",
    base_url="https://devapp.avocavo.app",  # Dev environment
    timeout=60  # Custom timeout
)

# Check API health
health = client.health_check()
print(f"API Status: {health['status']}")
print(f"Cache Hit Rate: {health['cache']['hit_rate']}")
```

### User Management
```python
# Check login status
if av.is_logged_in():
    user = av.get_current_user()
    print(f"Logged in as: {user['email']}")
else:
    print("Please login: av.login()")  # OAuth browser login

# Login with different provider
av.login(provider="github")  # GitHub OAuth instead of Google

# Logout
result = av.logout()
print(result['message'])  # "Successfully logged out"
```

## 🔍 What Information You Get

The Avocavo Nutrition API provides comprehensive nutrition data with USDA verification:

### Core Nutrition Facts
- **Calories** - Energy content
- **Macronutrients** - Protein, carbohydrates, total fat
- **Fiber & Sugar** - Detailed carbohydrate breakdown  
- **Minerals** - Sodium, calcium, iron
- **Fats** - Saturated fat, cholesterol

### USDA Verification
- **Real FDC IDs** from USDA FoodData Central
- **Verification URLs** for manual checking
- **Data source types** (Foundation, SR Legacy, Survey, Branded)
- **Confidence scores** for match quality

### Performance Metrics
- **Cache status** - Whether data came from cache
- **Response times** - API performance tracking
- **Processing method** - How the ingredient was matched

### Example Response
```python
result = av.analyze_ingredient("1 cup cooked brown rice")

# Nutrition data
print(f"Calories: {result.nutrition.calories}")           # 216.0
print(f"Protein: {result.nutrition.protein}g")            # 5.0
print(f"Carbs: {result.nutrition.carbs}g")               # 45.0
print(f"Fiber: {result.nutrition.fiber}g")               # 3.5

# USDA verification
print(f"FDC ID: {result.usda_match.fdc_id}")             # 168880
print(f"Description: {result.usda_match.description}")    # "Rice, brown, long-grain, cooked"
print(f"Data Type: {result.usda_match.data_type}")       # "SR Legacy"
print(f"Verify: {result.verification_url}")              # USDA verification link

# Performance
print(f"From Cache: {result.from_cache}")                # True/False
print(f"Response Time: {result.processing_time_ms}ms")   # 45.2
print(f"Confidence: {result.confidence_score}%")         # 95
```

## 📚 Documentation

- **[Complete API Documentation](https://docs.avocavo.app)** - Full reference
- **[Get API Key](https://nutrition.avocavo.app)** - Sign up for free
- **[GitHub Repository](https://github.com/avocavo/nutrition-api-python)** - Source code
- **[Support](mailto:api-support@avocavo.com)** - Get help

## 🤝 Support

- **Email**: [api-support@avocavo.com](mailto:api-support@avocavo.com)
- **Documentation**: [docs.avocavo.app](https://docs.avocavo.app)
- **Status Page**: [status.avocavo.app](https://status.avocavo.app)
- **Feature Requests**: [GitHub Issues](https://github.com/avocavo/nutrition-api-python/issues)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ by the Avocavo team**

*Get started in 30 seconds: `pip install avocavo-nutrition`*