from enum import Enum


class Gpt(Enum):
    """Enumeration class for GPT models.

    Attributes:
        MODEL_GPT_WHISPER_1 (str): Pretrained model name for GPT Whisper-1
        MODEL_GPT_3_5_TURBO (str): Pretrained model name for GPT 3.5 Turbo
        MODEL_GPT_3_5_TURBO_16K (str): Pretrained model name for GPT 3.5 Turbo 16K
        MODEL_GPT_4 (str): Pretrained model name for GPT 4
        MODEL_GPT_4_32K (str): Pretrained model name for GPT 4 32K
        MODEL_DALL_E (str): Pretrained model name for DALL-E

    """
    MODEL_GPT_WHISPER_1 = "whisper-1"
    MODEL_GPT_3_5_TURBO = "gpt-3.5-turbo"
    MODEL_GPT_3_5_TURBO_16K = "gpt-3.5-turbo-16k"
    MODEL_GPT_4 = "gpt-4"
    MODEL_GPT_4_32K = "gpt-4-32k"
    MODEL_DALL_E = "dall-e-3"
