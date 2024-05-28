from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    OVERRIDE_INPUT: bool = True
    OVERRIDE_OUTPUT: bool = True

    INPUT_PATH: Path
    OUTPUT_PATH: Path

    STYLESHEET: Literal['CERULEAN', 'CERULEAN', 'COSMO', 'CYBORG', 'DARKLY', 'FLATLY', 'JOURNAL',
                        'LITERA', 'LUMEN', 'LUX', 'MATERIA', 'MINTY', 'MORPH', 'PULSE', 'QUARTZ',
                        'SANDSTONE', 'SIMPLEX', 'SKETCHY', 'SLATE', 'SOLAR', 'SPACELAB', 'SUPERHERO',
                        'UNITED', 'VAPOR', 'YETI', 'ZEPHYR']

    PLOT_TITLE: str
    PLOT_XAXIS_LABEL: str
    PLOT_YAXIS_LABEL: str
    PLOT_FONT_SIZE: int

    def create_folders(self):
        if not self.INPUT_PATH.exists():
            self.INPUT_PATH.mkdir(parents=True, exist_ok=True)

        if not self.OUTPUT_PATH.exists():
            self.OUTPUT_PATH.mkdir(parents=True, exist_ok=True)


config = Config(_env_file='.env')
config.create_folders()
