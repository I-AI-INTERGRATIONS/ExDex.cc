#!/usr/bin/env python3
"""
Configuration loader and validator for ExDex.cc
Reads JOHN.ini and provides configuration access with validation
"""

import configparser
import os
import sys
from typing import Any, Dict, List, Optional


class ExDexConfig:
    """Configuration loader for ExDex backend services"""
    
    # Keywords that indicate sensitive configuration values
    SENSITIVE_KEYWORDS = ['key', 'secret', 'password']
    
    def __init__(self, config_file: str = "JOHN.ini"):
        """
        Initialize configuration loader
        
        Args:
            config_file: Path to the configuration file (default: JOHN.ini)
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        
        if not os.path.exists(config_file):
            raise FileNotFoundError(
                f"Configuration file '{config_file}' not found. "
                f"Please copy JOHN.ini.example to JOHN.ini and configure it."
            )
        
        self.config.read(config_file)
        self._validate_config()
    
    def _validate_config(self):
        """Validate that required configuration sections and keys exist"""
        required_sections = [
            'SERVER',
            'BLOCKCHAIN_ETH',
            'LOGGING',
            'SECURITY'
        ]
        
        missing_sections = [
            section for section in required_sections 
            if not self.config.has_section(section)
        ]
        
        if missing_sections:
            raise ValueError(
                f"Missing required configuration sections: {', '.join(missing_sections)}"
            )
        
        # Check for unchanged placeholder values
        warnings = []
        
        # Check BLOCKCHAIN_ETH section if it exists
        if self.config.has_section('BLOCKCHAIN_ETH'):
            infura_url = self.config.get('BLOCKCHAIN_ETH', 'infura_url', fallback='')
            if infura_url.startswith('https://mainnet.infura.io/v3/YOUR_'):
                warnings.append("BLOCKCHAIN_ETH.infura_url still contains placeholder value")
        
        # Check SECURITY section if it exists
        if self.config.has_section('SECURITY'):
            jwt_secret = self.config.get('SECURITY', 'jwt_secret', fallback='')
            if 'CHANGE_ME' in jwt_secret:
                warnings.append("SECURITY.jwt_secret should be changed from default")
        
        # Check PAYMENT_COINPAYMENTS section if it exists
        if self.config.has_section('PAYMENT_COINPAYMENTS'):
            public_key = self.config.get('PAYMENT_COINPAYMENTS', 'public_key', fallback='')
            if 'YOUR_' in public_key:
                warnings.append("PAYMENT_COINPAYMENTS.public_key contains placeholder")
        
        if warnings:
            print("Configuration warnings:", file=sys.stderr)
            for warning in warnings:
                print(f"  - {warning}", file=sys.stderr)
    
    def get(self, section: str, key: str, fallback: Optional[str] = None) -> Optional[str]:
        """
        Get a configuration value
        
        Args:
            section: Configuration section
            key: Configuration key
            fallback: Default value if key not found
            
        Returns:
            Configuration value or fallback (can be None)
        """
        # Check environment variable override first
        # Empty strings from env vars are treated as intentional values
        env_key = f"{section}_{key}".upper()
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value
        
        return self.config.get(section, key, fallback=fallback)
    
    def getint(self, section: str, key: str, fallback: Optional[int] = None) -> Optional[int]:
        """Get an integer configuration value"""
        # Check environment variable override first
        env_key = f"{section}_{key}".upper()
        env_value = os.getenv(env_key)
        if env_value is not None:
            try:
                return int(env_value)
            except (ValueError, TypeError):
                pass  # Fall through to config file
        
        # Try to get from config file
        try:
            return self.config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def getfloat(self, section: str, key: str, fallback: Optional[float] = None) -> Optional[float]:
        """Get a float configuration value"""
        # Check environment variable override first
        env_key = f"{section}_{key}".upper()
        env_value = os.getenv(env_key)
        if env_value is not None:
            try:
                return float(env_value)
            except (ValueError, TypeError):
                pass  # Fall through to config file
        
        # Try to get from config file
        try:
            return self.config.getfloat(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def getboolean(self, section: str, key: str, fallback: Optional[bool] = None) -> Optional[bool]:
        """
        Get a boolean configuration value
        
        Environment variables are considered True if they are: true, yes, 1, on
        and False if they are: false, no, 0, off (case-insensitive)
        """
        # Check environment variable override first
        env_key = f"{section}_{key}".upper()
        env_value = os.getenv(env_key)
        if env_value is not None:
            env_lower = env_value.lower()
            if env_lower in ('true', 'yes', '1', 'on'):
                return True
            elif env_lower in ('false', 'no', '0', 'off'):
                return False
            # If not recognized, fall through to config file
        
        # Try to get from config file
        try:
            return self.config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get all key-value pairs from a section
        
        Args:
            section: Configuration section name
            
        Returns:
            Dictionary of configuration values
        """
        if not self.config.has_section(section):
            return {}
        return dict(self.config.items(section))
    
    def has_section(self, section: str) -> bool:
        """Check if a section exists"""
        return self.config.has_section(section)
    
    def sections(self) -> List[str]:
        """Get all section names"""
        return self.config.sections()


def main():
    """CLI tool to validate and display configuration"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ExDex Configuration Tool')
    parser.add_argument('--file', default='JOHN.ini', help='Configuration file path')
    parser.add_argument('--validate', action='store_true', help='Validate configuration')
    parser.add_argument('--show', action='store_true', help='Show all configuration (redacted)')
    parser.add_argument('--section', help='Show specific section')
    
    args = parser.parse_args()
    
    try:
        config = ExDexConfig(args.file)
        
        if args.validate:
            print(f"Configuration file '{args.file}' is valid!")
            print(f"Sections found: {', '.join(config.sections())}")
            return 0
        
        if args.section:
            section_data = config.get_section(args.section)
            if section_data:
                print(f"[{args.section}]")
                for key, value in section_data.items():
                    # Redact sensitive values
                    if any(sensitive in key.lower() for sensitive in ExDexConfig.SENSITIVE_KEYWORDS):
                        value = '***REDACTED***'
                    print(f"{key} = {value}")
            else:
                print(f"Section '{args.section}' not found")
            return 0
        
        if args.show:
            print("Configuration sections and keys (sensitive values redacted):")
            for section in config.sections():
                print(f"\n[{section}]")
                section_data = config.get_section(section)
                for key, value in section_data.items():
                    if any(sensitive in key.lower() for sensitive in ExDexConfig.SENSITIVE_KEYWORDS):
                        value = '***REDACTED***'
                    print(f"  {key} = {value}")
            return 0
        
        parser.print_help()
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
