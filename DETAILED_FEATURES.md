# 🥑 Avocavo Python SDK - Detailed Features Guide

## 🎯 What Makes This SDK Unique

The Avocavo Python SDK is designed for **production applications** that need seamless nutrition data integration. Unlike simple API wrappers, this SDK provides:

### 🔐 **Smart Authentication System**
```python
# One-time OAuth login - no more API key management!
import avocavo_nutrition as av
av.login()  # Opens browser for Google/GitHub OAuth

# Now use anywhere in your code - no API keys needed
result = av.analyze_ingredient("2 cups flour")
```

**Why This Matters:**
- **Secure credential storage** using the system keyring
- **No hardcoded API keys** in your source code
- **Automatic token refresh** - never worry about expiration
- **Team-friendly** - each developer logs in once

### ⚡ **Production-Ready Performance**
```python
# Batch processing for high-throughput applications
batch = av.analyze_batch([
    "1 cup quinoa", "2 tbsp olive oil", "4 oz salmon", "1 cup spinach"
])
print(f"Success rate: {batch.success_rate}%")  # Typically 95%+
```

**Performance Features:**
- **94%+ cache hit rate** = sub-second responses
- **8,000+ requests/hour** throughput capability  
- **Intelligent batching** reduces API calls by 60%
- **Automatic retry logic** with exponential backoff

### 🧠 **Advanced Nutrition Intelligence**
```python
# Handles complex ingredient parsing automatically
result = av.analyze_ingredient("2 cups all-purpose flour, sifted")
print(f"Recognized: {result.parsed_ingredient.quantity} {result.parsed_ingredient.unit}")
print(f"Base food: {result.parsed_ingredient.food_name}")
print(f"Modifiers: {result.parsed_ingredient.modifiers}")  # ['sifted']

# Complete nutrition profile with 30+ nutrients
nutrition = result.nutrition
print(f"Calories: {nutrition.calories}")
print(f"Protein: {nutrition.protein}g")
print(f"Vitamin C: {nutrition.vitamin_c}mg")  # Micronutrients included
print(f"Calcium: {nutrition.calcium}mg")
```

### 📊 **Enterprise Account Management**
```python
# Real-time usage monitoring
account = av.get_account_usage()
print(f"Plan: {account.plan_name}")
print(f"Usage: {account.usage.current_month}/{account.usage.monthly_limit}")
print(f"Cost this month: ${account.usage.estimated_cost}")
print(f"Reset date: {account.usage.reset_date}")

# Usage optimization suggestions
if account.usage.efficiency_score < 80:
    print("💡 Suggestions:", account.optimization_tips)
```

### 🔬 **Scientific Data Verification**
```python
result = av.analyze_ingredient("1 cup brown rice")

# USDA FoodData Central integration
print(f"USDA ID: {result.usda_match.fdc_id}")
print(f"Data source: {result.usda_match.data_type}")  # Foundation/SR Legacy/Survey
print(f"Verification URL: {result.verification_url}")
print(f"Confidence score: {result.confidence_score}%")

# Publication references
print(f"Source publication: {result.usda_match.publication_date}")
print(f"Study type: {result.usda_match.study_method}")
```

## 🏗️ **Real-World Use Cases**

### 1. Recipe App with Dynamic Nutrition
```python
class RecipeNutritionCalculator:
    def __init__(self):
        av.login()  # One-time setup
    
    def calculate_nutrition(self, ingredients, servings=1):
        """Calculate nutrition for any recipe with caching"""
        recipe = av.analyze_recipe(ingredients, servings)
        
        return {
            'per_serving': {
                'calories': recipe.nutrition.per_serving.calories,
                'macros': {
                    'protein': recipe.nutrition.per_serving.protein,
                    'carbs': recipe.nutrition.per_serving.carbs,
                    'fat': recipe.nutrition.per_serving.fat
                },
                'micros': {
                    'vitamin_c': recipe.nutrition.per_serving.vitamin_c,
                    'iron': recipe.nutrition.per_serving.iron,
                    'calcium': recipe.nutrition.per_serving.calcium
                }
            },
            'usda_verified': len(recipe.usda_matches),
            'confidence': recipe.average_confidence,
            'processing_time': recipe.processing_time_ms
        }

# Usage in Flask/Django app
@app.route('/recipe/nutrition', methods=['POST'])
def get_recipe_nutrition():
    calculator = RecipeNutritionCalculator()
    data = request.json
    
    nutrition = calculator.calculate_nutrition(
        ingredients=data['ingredients'],
        servings=data.get('servings', 1)
    )
    
    return jsonify(nutrition)
```

### 2. Meal Planning Service
```python
class MealPlanOptimizer:
    def __init__(self):
        av.login()
        
    def optimize_weekly_plan(self, meals, dietary_goals):
        """Optimize meals for nutritional goals"""
        total_nutrition = {'calories': 0, 'protein': 0, 'fiber': 0}
        
        # Batch analyze all meals efficiently
        all_ingredients = []
        for meal in meals:
            all_ingredients.extend(meal['ingredients'])
        
        batch_results = av.analyze_batch(all_ingredients)
        
        # Calculate totals and suggest swaps
        for meal in meals:
            meal_nutrition = self._calculate_meal_nutrition(meal, batch_results)
            self._suggest_optimizations(meal, meal_nutrition, dietary_goals)
            
        return self._generate_shopping_list(meals)
```

### 3. Fitness Tracker Integration
```python
class NutritionTracker:
    def __init__(self):
        av.login()
        
    def log_food_entry(self, user_id, food_description, timestamp):
        """Log food with automatic nutrition calculation"""
        result = av.analyze_ingredient(food_description)
        
        if result.success:
            # Store in database with rich metadata
            food_entry = {
                'user_id': user_id,
                'timestamp': timestamp,
                'original_input': food_description,
                'parsed_food': result.parsed_ingredient.food_name,
                'quantity': result.parsed_ingredient.quantity,
                'unit': result.parsed_ingredient.unit,
                'nutrition': result.nutrition.to_dict(),
                'usda_fdc_id': result.usda_match.fdc_id,
                'confidence_score': result.confidence_score,
                'verification_url': result.verification_url
            }
            
            self.database.save_food_entry(food_entry)
            return food_entry
        else:
            # Handle unrecognized foods
            return self._handle_unknown_food(food_description)
```

## 🎛️ **Configuration & Customization**

### Environment Setup
```python
# Multiple authentication methods
av.login("user@example.com", "password")  # Direct login
av.login()  # OAuth (opens browser)

# API key fallback
from avocavo_nutrition import NutritionAPI
client = NutritionAPI(api_key="your_key")

# Environment variable
os.environ['AVOCAVO_API_KEY'] = 'your_key'
result = av.analyze_ingredient("1 cup rice")  # Auto-detects
```

### Advanced Options
```python
# Custom configuration
av.configure({
    'cache_ttl': 3600,  # Cache for 1 hour
    'timeout': 30,      # 30 second timeout
    'retry_count': 3,   # Retry failed requests 3 times
    'verify_ssl': True, # SSL verification
    'user_agent': 'MyApp/1.0'
})

# Regional data preferences
result = av.analyze_ingredient("1 cup rice", options={
    'prefer_organic': True,
    'region': 'US',  # Prefer US food data
    'data_source': 'foundation'  # Only use USDA Foundation data
})
```

## 📈 **Performance Monitoring**

```python
# Built-in performance tracking
result = av.analyze_ingredient("1 cup chicken")

print(f"Cache hit: {result.cache_hit}")
print(f"Processing time: {result.processing_time_ms}ms")
print(f"API credits used: {result.credits_consumed}")

# Batch operation efficiency
batch = av.analyze_batch(ingredients)
print(f"Batch efficiency: {batch.efficiency_score}%")
print(f"Cache hit rate: {batch.cache_hit_rate}%")
print(f"Total credits saved: {batch.credits_saved}")
```

## 🛡️ **Error Handling & Reliability**

```python
from avocavo_nutrition import ApiError, RateLimitError, AuthenticationError

try:
    result = av.analyze_ingredient("mystery food")
    
    if result.success:
        return result.nutrition
    else:
        # Graceful degradation
        return estimate_nutrition_fallback(ingredient)
        
except RateLimitError as e:
    # Handle rate limits gracefully
    wait_time = e.retry_after_seconds
    logger.warning(f"Rate limited, retry in {wait_time}s")
    
except AuthenticationError:
    # Re-authenticate automatically
    av.login()
    return av.analyze_ingredient(ingredient)
    
except ApiError as e:
    logger.error(f"API error: {e.message}")
    return None
```

## 🔄 **Migration from Other APIs**

```python
# Easy migration from other nutrition APIs
def migrate_from_edamam(edamam_results):
    """Convert Edamam results to Avocavo format"""
    migrated_results = []
    
    for item in edamam_results:
        # Use Avocavo's more accurate data
        result = av.analyze_ingredient(item['ingredient'])
        
        if result.success:
            migrated_results.append({
                'ingredient': result.ingredient,
                'calories': result.nutrition.calories,
                'nutrients': result.nutrition.to_dict(),
                'usda_verified': bool(result.usda_match),
                'confidence': result.confidence_score
            })
    
    return migrated_results
```

This Python SDK is designed for developers building **production nutrition applications** who need reliable, accurate, and scalable nutrition data with minimal integration effort.
