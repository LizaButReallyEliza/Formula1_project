from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    A configuration class for managing application settings using Pydantic.

    Attributes:
        db_user (str): Database username.
        db_password (str): Database password.
        db_host (str): Host address of the database server.
        db_port (int): Port number for the database connection.
        db_name (str): Name of the database.
        db_owner (str): The owner of the database.

    Configurations:
        env_file (str): Specifies the path to the `.env` file for loading environment variables.
    """

    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    db_owner: str

    class Config:
        """
        Configuration for Pydantic settings.

        Attributes:
            env_file (str): Path to the environment file that contains key-value pairs for settings.
        """
        env_file = ".env"

    @property
    def database_url(self) -> str:
        """
        Constructs the database URL for connecting to the PostgreSQL database.

        Returns:
            str: A complete database connection URL in the format
                 'postgresql+asyncpg://user:password@host:port/db_name'.
        """
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

# Initialize the settings object, which will automatically load values from the .env file
settings = Settings()