#!/usr/bin/env python3
"""
Configuration loader and validator for ExDex.cc
Reads JOHN.ini and provides configuration access with validation
"""

import configparser
import os
import sys
from typing import Any, Dict, Optional


class ExDexConfig:
    """Configuration loader for ExDex backend services"""
    
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
        
        missing_sections = []
        for section in required_sections:
            if not self.config.has_section(section):
                missing_sections.append(section)
        
        if missing_sections:
            raise ValueError(
                f"Missing required configuration sections: {', '.join(missing_sections)}"
            )
        
        # Check for unchanged placeholder values
        warnings = []
        
        if self.config.get('BLOCKCHAIN_ETH', 'infura_url').startswith('https://mainnet.infura.io/v3/YOUR_'):
            warnings.append("BLOCKCHAIN_ETH.infura_url still contains placeholder value")
        
        if 'CHANGE_ME' in self.config.get('SECURITY', 'jwt_secret', fallback=''):
            warnings.append("SECURITY.jwt_secret should be changed from default")
        
        if self.config.has_section('PAYMENT_COINPAYMENTS'):
            if 'YOUR_' in self.config.get('PAYMENT_COINPAYMENTS', 'public_key', fallback=''):
                warnings.append("PAYMENT_COINPAYMENTS.public_key contains placeholder")
        
        if warnings:
            print("Configuration warnings:", file=sys.stderr)
            for warning in warnings:
                print(f"  - {warning}", file=sys.stderr)
    
    def get(self, section: str, key: str, fallback: Optional[str] = None) -> str:
        """
        Get a configuration value
        
        Args:
            section: Configuration section
            key: Configuration key
            fallback: Default value if key not found
            
        Returns:
            Configuration value or fallback
        """
        # Check environment variable override first
        env_key = f"{section}_{key}".upper()
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value
        
        return self.config.get(section, key, fallback=fallback)
    
    def getint(self, section: str, key: str, fallback: Optional[int] = None) -> int:
        """Get an integer configuration value"""
        value = self.get(section, key, str(fallback) if fallback is not None else None)
        return int(value) if value is not None else fallback
    
    def getfloat(self, section: str, key: str, fallback: Optional[float] = None) -> float:
        """Get a float configuration value"""
        value = self.get(section, key, str(fallback) if fallback is not None else None)
        return float(value) if value is not None else fallback
    
    def getboolean(self, section: str, key: str, fallback: bool = False) -> bool:
        """Get a boolean configuration value"""
        value = self.get(section, key, str(fallback))
        return value.lower() in ('true', 'yes', '1', 'on')
    
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
    
    def sections(self) -> list:
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
                    if any(sensitive in key.lower() for sensitive in ['key', 'secret', 'password']):
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
                    if any(sensitive in key.lower() for sensitive in ['key', 'secret', 'password']):
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
