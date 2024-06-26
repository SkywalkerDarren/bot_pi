import dataclasses
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
CONFIG_JSON_PATH = os.path.join(PROJECT_ROOT, "config", "config.json")
MODELS_PATH = os.path.join(PROJECT_ROOT, "models")
ASSETS_PATH = os.path.join(PROJECT_ROOT, "assets")


@dataclasses.dataclass
class RecorderConfig:
    sample_rate: int
    channels: int
    width: int
    chunk: int


@dataclasses.dataclass
class AnthropicConfig:
    key: str
    model: str


@dataclasses.dataclass
class OpenAIConfig:
    key: str
    chat_model: str
    voice: str
    tts_model: str


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
class OpenWakeupWordConfig:
    model_name: str
    model_type: str
    sensitivity: float


@dataclasses.dataclass
class Config:
    recorder: RecorderConfig
    openai: OpenAIConfig
    anthropic: AnthropicConfig
    azure_speech: AzureConfig
    google: GoogleConfig
    open_wakeup_word: OpenWakeupWordConfig


with open(CONFIG_JSON_PATH, "r") as f:
    data = json.load(f)
    CONFIG = Config(
        recorder=RecorderConfig(**data.get("recorder", {})),
        openai=OpenAIConfig(**data.get("openai", {})),
        anthropic=AnthropicConfig(**data.get("anthropic", {})),
        azure_speech=AzureConfig(**data.get("azure_speech", {})),
        google=GoogleConfig(**data.get("google", {})),
        open_wakeup_word=OpenWakeupWordConfig(**data.get("open_wakeup_word", {}))
    )
