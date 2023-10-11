from .cyberdolphin_gradio import CyberDolphinGradioApi
from .cyberdolphin_openai_advanced import CyberdolphinOpenAIAdvanced
from .cyberdolphin_openai_simple import CyberdolphinOpenAISimple
from .cyberdolphin_openai_compatible import CyberdolphinOpenAICompatible

NODE_CLASS_MAPPINGS = {
    "🐬 Gradio ChatInterface": CyberDolphinGradioApi,
    "🐬 OpenAI Simple": CyberdolphinOpenAISimple,
    "🐬 OpenAI Advanced": CyberdolphinOpenAIAdvanced,
    "🐬 OpenAI Compatible": CyberdolphinOpenAICompatible,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CyberDolphin Gradio": "🐬 CyberDolphin Gradio",
    "CyberDolphin GPT-3.5 (Simple)": "🐬 CyberDolphin GPT-3.5 (Simple)",
    "CyberDolphin OpenAI (Advanced)": "🐬 CyberDolphin OpenAI (Advanced)",
    "CyberDolphin OpenAI Compatible": "🐬 CyberDolphin OpenAI Compatible",
}
