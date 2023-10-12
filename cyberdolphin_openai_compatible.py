from .openai_client import OpenAiClient
from .settings import load_settings


class CyberdolphinOpenAICompatible:

    @classmethod
    def INPUT_TYPES(s):
        all_settings = load_settings()
        prompt_templates = all_settings['prompt_templates']
        default_user_prompt = all_settings['example_user_prompt']
        available_apis = [a for a in all_settings['openai_compatible']]
        available_templates = [t for t in prompt_templates]
        default_model = all_settings['openai_compatible']['default']['model']

        return {
            "required": {
                "api": (available_apis, {
                    "default": "default"
                }),
                "prompt_template": (available_templates, {
                    "default": 'default'
                }),
                "model": ("STRING", {
                    "default": default_model
                }),
                "user_prompt": ("STRING", {
                    "multiline": True,
                    "default": default_user_prompt
                }),
                "temperature": ("FLOAT", {
                    "default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01,
                }),
            },
            "optional": {
                "top_p": ("FLOAT", {
                    "default": 1.0, "min": 0.001, "max": 1.0, "step": 0.01,
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("gpt_response",)
    FUNCTION = "generate"
    CATEGORY = "🐬 CyberDolphin"

    def generate(self, api: str, prompt_template: str, model: str, temperature: float | None = None,
                 top_p: float | None = None, user_prompt=""):
        this_prompt = load_settings()['prompt_templates'][prompt_template]
        system_content = this_prompt['system']
        user_content = f"{this_prompt['prefix']} {user_prompt} {this_prompt['suffix']}"

        response = OpenAiClient.complete(
            key=api,
            model=model,
            temperature=temperature,
            top_p=top_p,
            system_content=system_content,
            user_content=user_content)

        return (f'{response.choices[0].message.content}',)
