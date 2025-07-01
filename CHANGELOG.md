# Changelog

All notable changes to the Avocavo Nutrition API Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-07-01

### Added
- Initial release of the Avocavo Nutrition API Python SDK
- Support for ingredient analysis with USDA verification
- Recipe nutrition calculation with per-serving breakdowns
- Batch processing capabilities for multiple ingredients
- Authentication via login credentials or API keys
- Secure credential storage using keyring
- Comprehensive error handling and validation
- Type hints for better development experience
- Complete nutrition data including macros, minerals, and vitamins
- USDA FoodData Central integration with verification URLs
- Performance metrics and caching information
- Account usage and limits tracking

### Features
- **NutritionAPI Client**: Main client class for API interactions
- **Authentication**: Multiple auth methods (login, API key, environment)
- **Ingredient Analysis**: Parse and analyze any ingredient with quantity
- **Recipe Analysis**: Calculate nutrition for complete recipes
- **Batch Processing**: Efficient processing of multiple ingredients
- **Data Models**: Comprehensive models for nutrition data, USDA matches, and results
- **Error Handling**: Specific exception classes for different error types
- **Caching**: Automatic caching for improved performance

### Technical Details
- Python 3.7+ support
- Dependencies: requests>=2.25.0, keyring>=23.0.0
- MIT License
- Cross-platform compatibility
- Modern packaging with pyproject.toml

### Documentation
- Complete README with examples and usage patterns
- API documentation and guides
- Real-world integration examples
- Troubleshooting guide