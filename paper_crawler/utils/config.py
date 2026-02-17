import os
import yaml
from typing import Dict, Any


class Config:
    """Configuration loader and manager."""

    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize configuration.

        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.

        Args:
            key: Configuration key (e.g., 'database.type')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_database_url(self) -> str:
        """
        Get database connection URL.

        Returns:
            SQLAlchemy database URL
        """
        db_type = self.get('database.type', 'sqlite')

        if db_type == 'sqlite':
            db_path = self.get('database.sqlite.path', 'papers.db')
            return f'sqlite:///{db_path}'
        elif db_type == 'mysql':
            host = self.get('database.mysql.host')
            port = self.get('database.mysql.port')
            user = self.get('database.mysql.user')
            password = self.get('database.mysql.password')
            database = self.get('database.mysql.database')
            return f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
        elif db_type == 'postgresql':
            host = self.get('database.postgresql.host')
            port = self.get('database.postgresql.port')
            user = self.get('database.postgresql.user')
            password = self.get('database.postgresql.password')
            database = self.get('database.postgresql.database')
            return f'postgresql://{user}:{password}@{host}:{port}/{database}'
        else:
            raise ValueError(f"Unsupported database type: {db_type}")


# Global config instance
config = Config()
