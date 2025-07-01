#!/usr/bin/env python3
"""
Avocavo Nutrition API Python SDK - Usage Examples

This file demonstrates various ways to use the Avocavo Nutrition API SDK.
Run individual examples or the entire file to see the SDK in action.
"""

import os
import sys
import avocavo_nutrition as av
from avocavo_nutrition import NutritionAPI, ApiError, AuthenticationError, RateLimitError

# Add some example data
EXAMPLE_INGREDIENTS = [
    "2 cups all-purpose flour",
    "1 cup whole milk", 
    "2 large eggs",
    "1 tbsp olive oil",
    "1 tsp salt",
    "6 oz salmon fillet",
    "1 cup cooked brown rice",
    "2 cups spinach leaves"
]

EXAMPLE_RECIPE = [
    "2 cups all-purpose flour",
    "1 cup whole milk",
    "2 large eggs",
    "1/4 cup sugar",
    "2 tbsp butter",
    "1 tsp baking powder",
    "1/2 tsp salt"
]

def example_1_basic_login():
    """Example 1: Basic login and ingredient analysis"""
    print("🔐 Example 1: Login and Basic Analysis")
    print("=" * 50)
    
    # Note: Replace with actual credentials for testing
    # av.login("your-email@example.com", "your-password")
    
    # For this example, we'll show the pattern
    print("Login pattern:")
    print("av.login('your-email@example.com', 'your-password')")
    print()
    
    # Analyze a single ingredient
    print("Analyzing: '2 cups chocolate chips'")
    print("result = av.analyze_ingredient('2 cups chocolate chips')")
    print("if result.success:")
    print("    print(f'Calories: {result.nutrition.calories}')")
    print("    print(f'USDA Match: {result.usda_match.description}')")
    print()

def example_2_api_key_usage():
    """Example 2: Using API key directly"""
    print("🔑 Example 2: API Key Usage")
    print("=" * 50)
    
    # Method 1: Direct API key
    print("# Method 1: Direct API key")
    print("client = NutritionAPI(api_key='your_api_key_here')")
    print("result = client.analyze_ingredient('1 cup rice')")
    print()
    
    # Method 2: Environment variable
    print("# Method 2: Environment variable")
    print("export AVOCAVO_API_KEY='your_api_key_here'")
    print("result = av.analyze_ingredient('1 cup rice')  # Auto-detects from env")
    print()

def example_3_recipe_analysis():
    """Example 3: Complete recipe analysis"""
    print("🍳 Example 3: Recipe Analysis")
    print("=" * 50)
    
    print("Recipe ingredients:")
    for ingredient in EXAMPLE_RECIPE:
        print(f"  - {ingredient}")
    print()
    
    print("Code example:")
    print("recipe = av.analyze_recipe([")
    for ingredient in EXAMPLE_RECIPE:
        print(f"    '{ingredient}',")
    print("], servings=8)")
    print()
    print("if recipe.success:")
    print("    print(f'Per serving: {recipe.nutrition.per_serving.calories} calories')")
    print("    print(f'Total recipe: {recipe.nutrition.total.calories} calories')")
    print("    print(f'Total ingredients analyzed: {len(recipe.results)}')")
    print()

def example_4_batch_processing():
    """Example 4: Batch processing (Starter+ plans)"""
    print("⚡ Example 4: Batch Processing")
    print("=" * 50)
    
    print("Batch ingredients:")
    for ingredient in EXAMPLE_INGREDIENTS[:4]:
        print(f"  - {ingredient}")
    print()
    
    print("Code example:")
    print("batch = av.analyze_batch([")
    for ingredient in EXAMPLE_INGREDIENTS[:4]:
        print(f"    '{ingredient}',")
    print("])")
    print()
    print("print(f'Success rate: {batch.success_rate}%')")
    print("for item in batch.results:")
    print("    if item.success:")
    print("        print(f'{item.ingredient}: {item.nutrition.calories} cal')")
    print()

def example_5_error_handling():
    """Example 5: Comprehensive error handling"""
    print("🛡️ Example 5: Error Handling")
    print("=" * 50)
    
    print("try:")
    print("    result = av.analyze_ingredient('mystery ingredient')")
    print("    if result.success:")
    print("        print(f'Found: {result.usda_match.description}')")
    print("    else:")
    print("        print(f'No match found: {result.error}')")
    print()        
    print("except RateLimitError as e:")
    print("    print(f'Rate limit exceeded: {e.limit} requests/month')")
    print("    print(f'Current usage: {e.usage}')")
    print("except AuthenticationError as e:")
    print("    print(f'Authentication failed: {e.message}')")
    print("except ApiError as e:")
    print("    print(f'API Error: {e.message}')")
    print()

def example_6_account_management():
    """Example 6: Account and usage management"""
    print("📊 Example 6: Account Management")
    print("=" * 50)
    
    print("# Check account status")
    print("account = av.get_account_usage()")
    print("print(f'Plan: {account.plan_name}')")
    print("print(f'Usage: {account.usage.current_month}/{account.usage.monthly_limit}')")
    print("print(f'Remaining: {account.usage.remaining}')")
    print()
    
    print("# Check login status")
    print("if av.is_logged_in():")
    print("    user = av.get_current_user()")
    print("    print(f'Logged in as: {user[\"email\"]}')")
    print("else:")
    print("    print('Not logged in')")
    print()

def example_7_real_world_recipe_app():
    """Example 7: Real-world recipe app integration"""
    print("🥘 Example 7: Recipe App Integration")
    print("=" * 50)
    
    print("def calculate_recipe_nutrition(ingredients, servings=1):")
    print("    \"\"\"Calculate nutrition for any recipe\"\"\"")
    print("    try:")
    print("        recipe = av.analyze_recipe(ingredients, servings)")
    print("        ")
    print("        if recipe.success:")
    print("            return {")
    print("                'calories_per_serving': recipe.nutrition.per_serving.calories,")
    print("                'protein_per_serving': recipe.nutrition.per_serving.protein,")
    print("                'carbs_per_serving': recipe.nutrition.per_serving.carbs,")
    print("                'fat_per_serving': recipe.nutrition.per_serving.fat,")
    print("                'total_calories': recipe.nutrition.total.calories,")
    print("                'usda_verified_count': len(recipe.usda_matches),")
    print("                'success_rate': f'{recipe.success_rate}%'")
    print("            }")
    print("        else:")
    print("            return {'error': 'Failed to analyze recipe'}")
    print("    except Exception as e:")
    print("        return {'error': str(e)}")
    print()
    print("# Usage:")
    print("nutrition = calculate_recipe_nutrition([")
    for ingredient in EXAMPLE_RECIPE[:4]:
        print(f"    '{ingredient}',")
    print("], servings=6)")
    print("print(nutrition)")
    print()

def example_8_fitness_tracker():
    """Example 8: Fitness tracker integration"""
    print("💪 Example 8: Fitness Tracker Integration") 
    print("=" * 50)
    
    print("def track_daily_nutrition(food_entries):")
    print("    \"\"\"Track daily nutrition from food entries\"\"\"")
    print("    totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}")
    print("    ")
    print("    for food in food_entries:")
    print("        try:")
    print("            result = av.analyze_ingredient(food)")
    print("            if result.success:")
    print("                totals['calories'] += result.nutrition.calories")
    print("                totals['protein'] += result.nutrition.protein")
    print("                totals['carbs'] += result.nutrition.carbs")
    print("                totals['fat'] += result.nutrition.fat")
    print("        except Exception as e:")
    print("            print(f'Error analyzing {food}: {e}')")
    print("    ")
    print("    return totals")
    print()
    print("# Daily food tracking")
    print("daily_foods = [")
    print("    '1 cup oatmeal',")
    print("    '1 medium banana',")
    print("    '6 oz grilled chicken breast',")
    print("    '2 cups steamed broccoli',")
    print("    '1 tbsp olive oil'")
    print("]")
    print("totals = track_daily_nutrition(daily_foods)")
    print("print(f'Daily totals: {totals}')")
    print()

def example_9_configuration():
    """Example 9: Advanced configuration"""
    print("⚙️ Example 9: Advanced Configuration")
    print("=" * 50)
    
    print("# Custom configuration")
    print("client = NutritionAPI(")
    print("    api_key='your_key',")
    print("    base_url='https://devapp.avocavo.app',  # Development environment")
    print("    timeout=60  # Custom timeout")
    print(")")
    print()
    print("# Health check")
    print("health = client.health_check()")
    print("print(f'API Status: {health[\"status\"]}')")
    print("print(f'Cache Hit Rate: {health[\"cache\"][\"hit_rate\"]}')")
    print()

def run_interactive_demo():
    """Run an interactive demo if credentials are available"""
    print("🎮 Interactive Demo")
    print("=" * 50)
    
    # Check if we can actually run examples
    api_key = os.getenv('AVOCAVO_API_KEY')
    if not api_key:
        print("⚠️  No API key found in environment.")
        print("To run the interactive demo, set your API key:")
        print("export AVOCAVO_API_KEY='your_api_key_here'")
        print()
        print("Or create a .env file with:")
        print("AVOCAVO_API_KEY=your_api_key_here")
        return
    
    print("✅ API key found! Running interactive demo...")
    
    try:
        # Test a simple ingredient
        result = av.analyze_ingredient("1 cup cooked rice")
        if result.success:
            print(f"✅ Successfully analyzed: {result.usda_match.description}")
            print(f"   Calories: {result.nutrition.calories}")
            print(f"   Protein: {result.nutrition.protein}g")
            print(f"   From cache: {result.from_cache}")
        else:
            print(f"❌ Analysis failed: {result.error}")
            
    except AuthenticationError:
        print("❌ Authentication failed. Check your API key.")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all examples"""
    print("🥑 Avocavo Nutrition API Python SDK - Examples")
    print("=" * 60)
    print()
    
    examples = [
        example_1_basic_login,
        example_2_api_key_usage, 
        example_3_recipe_analysis,
        example_4_batch_processing,
        example_5_error_handling,
        example_6_account_management,
        example_7_real_world_recipe_app,
        example_8_fitness_tracker,
        example_9_configuration
    ]
    
    for example in examples:
        example()
        print()
    
    # Run interactive demo if possible
    run_interactive_demo()
    
    print("📚 More Examples")
    print("=" * 50)
    print("- Documentation: https://docs.avocavo.app")
    print("- GitHub Repository: https://github.com/avocavo/nutrition-api-python")
    print("- API Dashboard: https://nutrition.avocavo.app")
    print("- Get API Key: https://nutrition.avocavo.app/register")

if __name__ == "__main__":
    main()