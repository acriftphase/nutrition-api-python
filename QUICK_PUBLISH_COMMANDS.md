# 🚀 Quick Publish Commands

## Prerequisites Complete ✅
- [x] Package built and validated
- [x] Publishing tools installed 
- [x] GitHub Actions workflow ready
- [x] Documentation and examples created

## 🔐 1. Setup PyPI Credentials

### Get API Tokens
1. **Test PyPI**: https://test.pypi.org/manage/account/token/
2. **Production PyPI**: https://pypi.org/manage/account/token/

### Configure Credentials
```bash
# Copy template
cp .pypirc.template ~/.pypirc

# Edit with your tokens
nano ~/.pypirc

# Secure the file
chmod 600 ~/.pypirc
```

## 🧪 2. Test Upload (REQUIRED FIRST)

```bash
# Activate virtual environment
source venv/bin/activate

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ avocavo-nutrition

# Verify import
python -c "import avocavo_nutrition; print(f'Version: {avocavo_nutrition.__version__}')"
```

## 🚀 3. Production Upload (After successful testing)

```bash
# Upload to Production PyPI
twine upload dist/*

# Test production installation
pip install avocavo-nutrition
python -c "import avocavo_nutrition; print('Success!')"
```

## 📦 Current Build Info
- **Package**: `avocavo-nutrition`
- **Version**: `1.0.0`
- **Files Ready**: 
  - `dist/avocavo_nutrition-1.0.0-py3-none-any.whl`
  - `dist/avocavo_nutrition-1.0.0.tar.gz`
- **Validation**: ✅ PASSED

## 🔄 GitHub Mirror Setup

### Required Secrets (in GitHub repo settings)
- `TEST_PYPI_API_TOKEN`: Your Test PyPI token
- `PYPI_API_TOKEN`: Your Production PyPI token

### Auto-publish triggers:
- **Version tags**: Push tags like `v1.0.0` for automatic publishing
- **Manual**: Use GitHub Actions "workflow_dispatch" for manual publishing

## 🛠️ Version Update Process

When ready for v1.0.1:

```bash
# 1. Update version in avocavo_nutrition/__init__.py
sed -i 's/__version__ = "1.0.0"/__version__ = "1.0.1"/' avocavo_nutrition/__init__.py

# 2. Update version in pyproject.toml
sed -i 's/version = "1.0.0"/version = "1.0.1"/' pyproject.toml

# 3. Rebuild
rm -rf build/ dist/ *.egg-info/
source venv/bin/activate
python -m build
twine check dist/*

# 4. Test and publish
twine upload --repository testpypi dist/*
twine upload dist/*
```

## 📋 Post-Publishing Checklist

After successful upload:
- [ ] Check PyPI page: https://pypi.org/project/avocavo-nutrition/
- [ ] Test installation: `pip install avocavo-nutrition`
- [ ] Verify import works
- [ ] Create GitHub release
- [ ] Update documentation
- [ ] Announce release

## 🆘 Emergency Commands

### If upload fails:
```bash
# Check what went wrong
twine check dist/*

# Re-validate package
python -m build
twine check dist/*

# Check credentials
twine upload --repository testpypi dist/* --verbose
```

### If version exists:
```bash
# Increment version
# Edit avocavo_nutrition/__init__.py and pyproject.toml
# Then rebuild and upload
```

## 🔗 Important Links

- **Test PyPI**: https://test.pypi.org/project/avocavo-nutrition/
- **Production PyPI**: https://pypi.org/project/avocavo-nutrition/
- **GitHub Actions**: Will be at https://github.com/avocavo/nutrition-api-python/actions