"""
Authentication module for Avocavo Nutrition API
Handles user login, logout, and API key management
Supports both email/password and OAuth browser login
"""

import os
import json
import keyring
import requests
import webbrowser
import time
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
    
    def login(self, email: str = None, password: str = None, provider: str = "google") -> Dict:
        """
        Login with email/password or OAuth browser login
        
        Args:
            email: User email (for email/password login)
            password: User password (for email/password login)
            provider: OAuth provider ("google" or "github") for browser login
            
        Returns:
            Dictionary with user info and API key
            
        Raises:
            AuthenticationError: If login fails
        """
        # If email and password provided, use traditional login
        if email and password:
            return self._login_with_password(email, password)
        
        # Otherwise use OAuth browser login
        return self._login_with_oauth(provider)
    
    def _login_with_password(self, email: str, password: str) -> Dict:
        """Traditional email/password login"""
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
                'logged_in_at': data.get('timestamp'),
                'login_method': 'password'
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
    
    def _login_with_oauth(self, provider: str) -> Dict:
        """OAuth browser login with Google or GitHub"""
        try:
            print(f"🔐 Initiating {provider.title()} OAuth login...")
            
            # Step 1: Initiate OAuth flow
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={"provider": provider},
                timeout=30
            )
            
            if response.status_code != 200:
                data = response.json() if response.content else {}
                raise AuthenticationError(data.get('error', f'Failed to initiate {provider} login'))
            
            auth_data = response.json()
            if not auth_data.get('success'):
                raise AuthenticationError(auth_data.get('error', 'OAuth initiation failed'))
            
            session_id = auth_data.get('session_id')
            oauth_url = auth_data.get('oauth_url')
            
            if not session_id or not oauth_url:
                raise AuthenticationError("Invalid OAuth response from server")
            
            # Step 2: Open browser for user authentication
            print(f"🌐 Opening browser for {provider.title()} authentication...")
            print(f"📋 If browser doesn't open automatically, visit: {oauth_url}")
            
            try:
                webbrowser.open(oauth_url)
            except Exception:
                print("⚠️  Could not open browser automatically")
            
            # Step 3: Poll for completion
            print("⏳ Waiting for authentication to complete...")
            max_attempts = 60  # 5 minutes timeout
            attempt = 0
            
            while attempt < max_attempts:
                try:
                    status_response = requests.get(
                        f"{self.base_url}/api/auth/status/{session_id}",
                        timeout=10
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        
                        if status_data.get('status') == 'completed':
                            # Success! Store credentials
                            api_token = status_data.get('api_token')
                            user_email = status_data.get('user_email')
                            
                            if api_token and user_email:
                                self._store_api_key(user_email, api_token)
                                
                                # Store user config
                                self._store_user_config({
                                    'email': user_email,
                                    'api_tier': 'developer',  # Default for OAuth users
                                    'logged_in_at': time.time(),
                                    'login_method': 'oauth',
                                    'oauth_provider': provider
                                })
                                
                                print(f"✅ Login successful! Welcome {user_email}")
                                
                                return {
                                    'success': True,
                                    'email': user_email,
                                    'api_tier': 'developer',
                                    'provider': provider,
                                    'message': f'{provider.title()} OAuth login successful'
                                }
                            else:
                                raise AuthenticationError("Invalid response from OAuth completion")
                        
                        elif status_data.get('status') == 'error':
                            raise AuthenticationError(status_data.get('error', 'OAuth authentication failed'))
                        
                        # Still pending, continue polling
                        if attempt == 0:
                            print("👆 Please complete authentication in your browser...")
                        elif attempt % 10 == 0:  # Show progress every 10 attempts
                            print("⏳ Still waiting for authentication...")
                    
                    elif status_response.status_code == 404:
                        raise AuthenticationError("OAuth session expired. Please try again.")
                
                except requests.exceptions.RequestException:
                    pass  # Network issues, continue trying
                
                time.sleep(5)  # Wait 5 seconds between polls
                attempt += 1
            
            raise AuthenticationError("OAuth login timed out. Please try again.")
            
        except AuthenticationError:
            raise
        except Exception as e:
            raise AuthenticationError(f"OAuth login failed: {str(e)}")
    
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


def login(email: str = None, password: str = None, provider: str = "google", base_url: str = "https://app.avocavo.app") -> Dict:
    """
    Login to Avocavo and store API key securely
    
    Args:
        email: Your email (for email/password login)
        password: Your password (for email/password login)
        provider: OAuth provider ("google" or "github") for browser login
        base_url: API base URL (defaults to production)
        
    Returns:
        Login result with user info
        
    Examples:
        import avocavo_nutrition as av
        
        # OAuth browser login (recommended)
        result = av.login()  # Opens browser for Google OAuth
        result = av.login(provider="github")  # Opens browser for GitHub OAuth
        
        # Email/password login (legacy)
        result = av.login("user@example.com", "password")
        
        if result['success']:
            print(f"Logged in as {result['email']}")
            
            # Now you can use the API without passing API key
            nutrition = av.analyze_ingredient("2 cups flour")
    """
    global _auth_manager
    _auth_manager = AuthManager(base_url)
    return _auth_manager.login(email, password, provider)


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