"""
Authentication module for Avocavo Nutrition API
Handles user login, logout, and API key management
"""

import os
import json
import keyring
import requests
from typing import Optional, Dict
from pathlib import Path
from .models import Account
from .exceptions import ApiError, AuthenticationError


class AuthManager:
    """Manages authentication and API key storage"""
    
    SERVICE_NAME = "avocavo-nutrition"
    CONFIG_DIR = Path.home() / ".avocavo"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    
    def __init__(self, base_url: str = "https://app.avocavo.app"):
        self.base_url = base_url.rstrip('/')
        self.config_dir = self.CONFIG_DIR
        self.config_file = self.CONFIG_FILE
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
    
    def login(self, email: str, password: str) -> Dict:
        """
        Login with email and password, store API key securely
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dictionary with user info and API key
            
        Raises:
            AuthenticationError: If login fails
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "email": email,
                    "password": password
                },
                timeout=30
            )
            
            if response.status_code == 401:
                raise AuthenticationError("Invalid email or password")
            elif response.status_code != 200:
                raise AuthenticationError(f"Login failed: {response.status_code}")
            
            data = response.json()
            
            if not data.get('success'):
                raise AuthenticationError(data.get('error', 'Login failed'))
            
            # Extract user info and API key
            user_info = data.get('user', {})
            api_key = user_info.get('api_key')
            
            if not api_key:
                raise AuthenticationError("No API key received")
            
            # Store API key securely
            self._store_api_key(email, api_key)
            
            # Store user config
            self._store_user_config({
                'email': email,
                'user_id': user_info.get('id'),
                'api_tier': user_info.get('api_tier', 'developer'),
                'logged_in_at': data.get('timestamp')
            })
            
            return {
                'success': True,
                'email': email,
                'api_tier': user_info.get('api_tier'),
                'api_key': api_key[:12] + "...",  # Masked for display
                'message': 'Successfully logged in'
            }
            
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Connection error: {str(e)}")
    
    def logout(self) -> Dict:
        """
        Logout current user and clear stored credentials
        
        Returns:
            Success message
        """
        config = self._load_user_config()
        
        if config and config.get('email'):
            # Remove stored API key
            try:
                keyring.delete_password(self.SERVICE_NAME, config['email'])
            except keyring.errors.PasswordDeleteError:
                pass  # Key was already removed
        
        # Remove config file
        if self.config_file.exists():
            self.config_file.unlink()
        
        return {
            'success': True,
            'message': 'Successfully logged out'
        }
    
    def get_current_user(self) -> Optional[Dict]:
        """
        Get current logged-in user info
        
        Returns:
            User info dictionary or None if not logged in
        """
        config = self._load_user_config()
        
        if not config or not config.get('email'):
            return None
        
        api_key = self._get_api_key(config['email'])
        
        if not api_key:
            return None
        
        return {
            'email': config['email'],
            'api_tier': config.get('api_tier'),
            'user_id': config.get('user_id'),
            'api_key': api_key,
            'logged_in_at': config.get('logged_in_at')
        }
    
    def get_api_key(self) -> Optional[str]:
        """
        Get stored API key for current user
        
        Returns:
            API key or None if not logged in
        """
        user = self.get_current_user()
        return user.get('api_key') if user else None
    
    def is_logged_in(self) -> bool:
        """Check if user is currently logged in"""
        return self.get_current_user() is not None
    
    def _store_api_key(self, email: str, api_key: str) -> None:
        """Store API key securely using keyring"""
        try:
            keyring.set_password(self.SERVICE_NAME, email, api_key)
        except Exception as e:
            # Fallback to config file if keyring fails
            print(f"Warning: Could not store API key securely: {e}")
            config = self._load_user_config() or {}
            config['api_key_fallback'] = api_key
            self._store_user_config(config)
    
    def _get_api_key(self, email: str) -> Optional[str]:
        """Retrieve API key securely"""
        try:
            return keyring.get_password(self.SERVICE_NAME, email)
        except Exception:
            # Fallback to config file
            config = self._load_user_config()
            return config.get('api_key_fallback') if config else None
    
    def _store_user_config(self, config: Dict) -> None:
        """Store user configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def _load_user_config(self) -> Optional[Dict]:
        """Load user configuration"""
        if not self.config_file.exists():
            return None
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None


# Global auth manager instance
_auth_manager = AuthManager()


def login(email: str, password: str, base_url: str = "https://app.avocavo.app") -> Dict:
    """
    Login to Avocavo and store API key securely
    
    Args:
        email: Your Avocavo account email
        password: Your Avocavo account password
        base_url: API base URL (defaults to production)
        
    Returns:
        Login result with user info
        
    Example:
        import avocavo_nutrition as av
        
        result = av.login("user@example.com", "password")
        if result['success']:
            print(f"Logged in as {result['email']}")
            
            # Now you can use the API without passing API key
            nutrition = av.analyze_ingredient("2 cups flour")
    """
    global _auth_manager
    _auth_manager = AuthManager(base_url)
    return _auth_manager.login(email, password)


def logout() -> Dict:
    """
    Logout and clear stored credentials
    
    Returns:
        Logout confirmation
        
    Example:
        result = av.logout()
        print(result['message'])  # "Successfully logged out"
    """
    return _auth_manager.logout()


def get_current_user() -> Optional[Dict]:
    """
    Get current logged-in user information
    
    Returns:
        User info dictionary or None if not logged in
        
    Example:
        user = av.get_current_user()
        if user:
            print(f"Logged in as: {user['email']}")
            print(f"Plan: {user['api_tier']}")
        else:
            print("Not logged in")
    """
    return _auth_manager.get_current_user()


def get_stored_api_key() -> Optional[str]:
    """
    Get stored API key for the current user
    
    Returns:
        API key or None if not logged in
    """
    return _auth_manager.get_api_key()


def is_logged_in() -> bool:
    """
    Check if user is currently logged in
    
    Returns:
        True if logged in, False otherwise
    """
    return _auth_manager.is_logged_in()


# For backwards compatibility with environment variables
def get_api_key_from_env() -> Optional[str]:
    """Get API key from environment variable"""
    return os.environ.get('AVOCAVO_API_KEY')


def get_api_key() -> Optional[str]:
    """
    Get API key from storage or environment
    Priority: logged-in user > environment variable
    """
    # First try logged-in user
    stored_key = get_stored_api_key()
    if stored_key:
        return stored_key
    
    # Fallback to environment variable
    return get_api_key_from_env()


if __name__ == "__main__":
    # Demo authentication
    print("🔐 Avocavo Nutrition API Authentication")
    print("=" * 40)
    
    user = get_current_user()
    if user:
        print(f"✅ Logged in as: {user['email']}")
        print(f"📊 Plan: {user['api_tier']}")
        print(f"🔑 API Key: {user.get('api_key', '')[:12]}...")
    else:
        print("❌ Not logged in")
        print("\nTo login:")
        print("  import avocavo_nutrition as av")
        print('  av.login("your@email.com", "password")')