import dataclasses
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
CONFIG_JSON_PATH = os.path.join(PROJECT_ROOT, "config", "config.json")
MODELS_PATH = os.path.join(PROJECT_ROOT, "models")


@dataclasses.dataclass
class RecorderConfig:
    sample_rate: int
    channels: int
    width: int
    chunk: int


@dataclasses.dataclass
class OpenAIConfig:
    key: str
    chat_model: str


@dataclasses.dataclass
class AzureConfig:
    region: str
    key: str
    voice_name: str
    recognition_language: str


@dataclasses.dataclass
class GoogleConfig:
    cx: str
    key: str
    cr: str
    gl: str
    num: int


@dataclasses.dataclass
class SpeakerConfig:
    sample_rate: int
    width: int
    channels: int

@dataclasses.dataclass
class OpenWakeupWordConfig:
    model_name: str
    model_type: str
    sensitivity: float

@dataclasses.dataclass
class Config:
    recorder: RecorderConfig
    speaker: SpeakerConfig
    openai: OpenAIConfig
    azure_speech: AzureConfig
    google: GoogleConfig
    open_wakeup_word: OpenWakeupWordConfig


with open(CONFIG_JSON_PATH, "r") as f:
    data = json.load(f)
    CONFIG = Config(
        recorder=RecorderConfig(**data.get("recorder", {})),
        speaker=SpeakerConfig(**data.get("speaker", {})),
        openai=OpenAIConfig(**data.get("openai", {})),
        azure_speech=AzureConfig(**data.get("azure_speech", {})),
        google=GoogleConfig(**data.get("google", {})),
        open_wakeup_word=OpenWakeupWordConfig(**data.get("open_wakeup_word", {}))
    )
