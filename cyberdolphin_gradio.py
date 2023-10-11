from gradio_client import Client

from .settings import load_settings


class CyberDolphinGradioApi:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "user_prompt": ("STRING", {
                    "default": load_settings()['example_user_prompt'],
                    "multiline": True,
                }),
                "llm_prompt": ([p for p in load_settings()['prompt_templates']], "STRING"),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("llm_response",)

    FUNCTION = "generate"

    # OUTPUT_NODE = False

    CATEGORY = "🐬 CyberDolphin"

    def generate(self, user_prompt="", llm_prompt: str = "default_prompt"):
        settings = load_settings()
        client_src = settings['gradio_chat_interface']['src']
        client = Client(client_src)
        prompt_prefix = settings['prompt_templates'][llm_prompt]['prefix']
        prompt_suffix = settings['prompt_templates'][llm_prompt]['suffix']

        prompt = f'{prompt_prefix} {user_prompt} {prompt_suffix}'
        result = client.predict(prompt, api_name="/chat")
        response = result
        return (f'{response}',)
