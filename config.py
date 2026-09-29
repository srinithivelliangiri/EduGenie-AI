import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


def load_env_file():
    """
    Simple .env file loader.
    This avoids needing python-dotenv, which helps
    keep the project compatible with Python 3.7.
    """

    if not ENV_FILE.exists():
        return

    try:
        with open(str(ENV_FILE), "r") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                if "=" not in line:
                    continue

                key, value = line.split("=", 1)

                key = key.strip()
                value = value.strip()

                # Remove surrounding quotes if present.
                if (
                    len(value) >= 2
                    and value[0] == '"'
                    and value[-1] == '"'
                ):
                    value = value[1:-1]

                if (
                    len(value) >= 2
                    and value[0] == "'"
                    and value[-1] == "'"
                ):
                    value = value[1:-1]

                # Don't overwrite an environment variable
                # that already exists.
                if key not in os.environ:
                    os.environ[key] = value

    except IOError:
        pass


load_env_file()


class Settings:
    def __init__(
        self,
        gemini_api_key="",
        gemini_model="gemini-2.5-flash",
        use_local_explainer=False,
        local_explainer_model="MBZUAI/LaMini-Flan-T5-783M",
        max_input_chars=20000
    ):
        self.gemini_api_key = gemini_api_key
        self.gemini_model = gemini_model
        self.use_local_explainer = use_local_explainer
        self.local_explainer_model = local_explainer_model
        self.max_input_chars = max_input_chars


_settings = None


def get_settings():
    global _settings

    if _settings is None:
        use_local = os.getenv(
            "USE_LOCAL_EXPLAINER",
            "false"
        ).lower() in (
            "true",
            "1",
            "yes",
            "on"
        )

        try:
            max_chars = int(
                os.getenv(
                    "MAX_INPUT_CHARS",
                    "20000"
                )
            )
        except ValueError:
            max_chars = 20000

        _settings = Settings(
            gemini_api_key=os.getenv(
                "GEMINI_API_KEY",
                ""
            ),
            gemini_model=os.getenv(
                "GEMINI_MODEL",
                "gemini-2.5-flash"
            ),
            use_local_explainer=use_local,
            local_explainer_model=os.getenv(
                "LOCAL_EXPLAINER_MODEL",
                "MBZUAI/LaMini-Flan-T5-783M"
            ),
            max_input_chars=max_chars
        )

    return _settings