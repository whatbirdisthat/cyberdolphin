from .openai_client import OpenAiClient
from .settings import load_settings


class CyberdolphinOpenAISimple:
    the_settings = None

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "user_prompt": ("STRING", {
                    "multiline": True,
                    "default": load_settings()['example_user_prompt']
                }),
                "temperature": ("FLOAT", {
                    "default": 1
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("gpt_response",)

    FUNCTION = "generate"

    # OUTPUT_NODE = False

    CATEGORY = "🐬 CyberDolphin"

    def generate(self, user_prompt="", temperature: float = 1.0):
        prompts = load_settings()['prompt_templates']
        system_content = prompts['gpt-3.5-turbo']['system']
        user_content = f"{prompts['gpt-3.5-turbo']['prefix']} {user_prompt} {prompts['gpt-3.5-turbo']['suffix']}"
        response = OpenAiClient.complete(
            key="openai_compatible",
            model=load_settings()['openai']['default_model'],
            temperature=temperature,
            top_p=1.0,
            system_content=system_content,
            user_content=user_content)

        return (f'{response.choices[0].message.content}',)
