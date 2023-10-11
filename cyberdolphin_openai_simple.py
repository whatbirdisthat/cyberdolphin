import openai
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
    def api_settings(self):
        openai_settings = load_settings()['openai']
        return openai_settings['api_base'], openai_settings['api_key'], openai_settings['organisation']

    def generate(self, user_prompt="", temperature: float = 1.0):
        prompts = load_settings()['prompt_templates']
        system_prompt = prompts['gpt-3.5-turbo']['system']
        user_content = f"{prompts['gpt-3.5-turbo']['prefix']} {user_prompt} {prompts['gpt-3.5-turbo']['suffix']}"

        # openai_settings = load_settings()['openai']
        # openai.api_base = openai_settings['api_base']
        # openai.api_key = openai_settings['api_key']
        # openai.organization = openai_settings['organisation']
        openai.api_base, openai.api_key, openai.organization = self.api_settings()

        response = openai.ChatCompletion.create(
            model=load_settings()['openai']['default_model'],
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        )

        return (f'{response.choices[0].message.content}',)
