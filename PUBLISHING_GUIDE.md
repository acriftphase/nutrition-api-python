# 🚀 PyPI Publishing Guide for avocavo-nutrition

This guide covers the complete process of publishing the Avocavo Nutrition API Python SDK to PyPI.

## 📋 Prerequisites

1. **PyPI Accounts**:
   - [Test PyPI Account](https://test.pypi.org/account/register/) (for testing)
   - [Production PyPI Account](https://pypi.org/account/register/) (for production)

2. **API Tokens**:
   - Generate API tokens from both PyPI accounts
   - Test PyPI: https://test.pypi.org/manage/account/token/
   - Production PyPI: https://pypi.org/manage/account/token/

## 🔐 Setup Credentials

### Option 1: Using .pypirc file (Recommended)

1. Copy the template:
   ```bash
   cp .pypirc.template ~/.pypirc
   ```

2. Edit `~/.pypirc` with your actual tokens:
   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = pypi-YOUR_PRODUCTION_TOKEN_HERE

   [testpypi]
   repository = https://test.pypi.org/legacy/
   username = __token__
   password = pypi-YOUR_TEST_TOKEN_HERE
   ```

3. Secure the file:
   ```bash
   chmod 600 ~/.pypirc
   ```

### Option 2: Environment Variables

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE
export TWINE_REPOSITORY_URL=https://test.pypi.org/legacy/  # For test PyPI
```

## 🏗️ Building the Package

The package is already built and validated! The build artifacts are:

- `dist/avocavo_nutrition-1.0.0-py3-none-any.whl` (wheel)
- `dist/avocavo_nutrition-1.0.0.tar.gz` (source distribution)

To rebuild if needed:

```bash
# Activate virtual environment
source venv/bin/activate

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build the package
python -m build

# Validate the package
twine check dist/*
```

## 🧪 Publishing to Test PyPI

**Always test first!**

```bash
# Activate virtual environment
source venv/bin/activate

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ avocavo-nutrition

# Test the package
python -c "import avocavo_nutrition; print('Package imported successfully!')"
```

## 🚀 Publishing to Production PyPI

**Only after successful testing!**

```bash
# Activate virtual environment
source venv/bin/activate

# Upload to Production PyPI
twine upload dist/*

# Verify installation
pip install avocavo-nutrition
python -c "import avocavo_nutrition; print(f'Version: {avocavo_nutrition.__version__}')"
```

## 📦 Package Information

- **Package Name**: `avocavo-nutrition`
- **Current Version**: `1.0.0`
- **Python Support**: 3.7+
- **Dependencies**: `requests>=2.25.0`, `keyring>=23.0.0`

## 🔄 Version Management

To release a new version:

1. Update version in `avocavo_nutrition/__init__.py`:
   ```python
   __version__ = "1.0.1"  # Increment version
   ```

2. Update version in `pyproject.toml`:
   ```toml
   version = "1.0.1"
   ```

3. Rebuild and publish:
   ```bash
   rm -rf build/ dist/ *.egg-info/
   python -m build
   twine check dist/*
   twine upload --repository testpypi dist/*  # Test first
   twine upload dist/*  # Then production
   ```

## 🛠️ Troubleshooting

### Common Issues

1. **"File already exists" error**:
   - PyPI doesn't allow re-uploading the same version
   - Increment the version number and rebuild

2. **Authentication failed**:
   - Check your API tokens
   - Verify .pypirc file permissions (should be 600)
   - Ensure you're using `__token__` as username

3. **Package validation failed**:
   - Run `twine check dist/*` to see specific issues
   - Check README.md formatting
   - Verify all required files are included

### Validation Commands

```bash
# Check package structure
tar -tzf dist/avocavo_nutrition-1.0.0.tar.gz

# Check wheel contents
unzip -l dist/avocavo_nutrition-1.0.0-py3-none-any.whl

# Validate metadata
twine check dist/*

# Test local installation
pip install dist/avocavo_nutrition-1.0.0-py3-none-any.whl
```

## 📊 Post-Publishing Checklist

After successful publishing:

- [ ] Verify package page on PyPI: https://pypi.org/project/avocavo-nutrition/
- [ ] Test installation: `pip install avocavo-nutrition`
- [ ] Check import: `python -c "import avocavo_nutrition"`
- [ ] Update documentation links
- [ ] Create GitHub release tag
- [ ] Announce the release

## 🔗 Useful Links

- **PyPI Package**: https://pypi.org/project/avocavo-nutrition/
- **Test PyPI**: https://test.pypi.org/project/avocavo-nutrition/
- **GitHub Repository**: https://github.com/avocavo/nutrition-api-python
- **Documentation**: https://docs.avocavo.app
- **API Dashboard**: https://nutrition.avocavo.app

## 📝 Notes

- The package includes both modern (`pyproject.toml`) and legacy (`setup.py`) configuration
- Built artifacts are validated with `twine check`
- Dependencies are pinned to minimum versions for maximum compatibility
- README.md is included as the long description on PyPI