#!/bin/bash
# Script to publish avocavo-nutrition package to PyPI

echo "🥑 Publishing Avocavo Nutrition API Python SDK to PyPI"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: setup.py not found. Run this from the package directory."
    exit 1
fi

# Step 1: Install build tools
echo "📦 Installing build tools..."
pip install --upgrade pip setuptools wheel twine

# Step 2: Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Step 3: Build the package
echo "🔨 Building package..."
python setup.py sdist bdist_wheel

# Step 4: Check the distribution
echo "🔍 Checking package..."
twine check dist/*

if [ $? -ne 0 ]; then
    echo "❌ Package check failed. Please fix issues above."
    exit 1
fi

echo "✅ Package built successfully!"
echo ""
echo "📋 What's in your package:"
ls -la dist/

echo ""
echo "🚀 Ready to publish! Choose one:"
echo ""
echo "   Test PyPI (recommended first):"
echo "   twine upload --repository testpypi dist/*"
echo ""
echo "   Production PyPI:"
echo "   twine upload dist/*"
echo ""
echo "📖 You'll need PyPI credentials. Get them at:"
echo "   - Test: https://test.pypi.org/account/register/"
echo "   - Production: https://pypi.org/account/register/"