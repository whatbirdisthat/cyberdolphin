import openai
from .settings import load_settings


class CyberdolphinOpenAIAdvanced:
    the_settings = None

    @classmethod
    def INPUT_TYPES(s):
        the_settings = load_settings()
        openai_settings = the_settings['openai']
        openai.api_base = openai_settings['api_base']
        openai.api_key = openai_settings['api_key']
        openai.organization = openai_settings['organisation']
        example_system_prompt = the_settings['prompt_templates']['gpt-3.5-turbo']['system']
        example_user_prompt = f"{the_settings['prompt_templates']['gpt-3.5-turbo']['prefix']}{the_settings['example_user_prompt']}{the_settings['prompt_templates']['gpt-3.5-turbo']['suffix']}"

        return {
            "required": {
                "model": ([m["id"] for m in openai.Model.list()['data']], {
                    "default": "gpt-3.5-turbo"}),
                "system_prompt": ('STRING', {
                    "multiline": True,
                    "default": example_system_prompt
                }),
                "user_prompt": ("STRING", {
                    "multiline": True,
                    "default": example_user_prompt
                }),
                "temperature": ("FLOAT", {
                    "default": 1
                }),
            },
            "optional": {
                "top_p": ("FLOAT", {
                    "default": None
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("gpt_response",)

    FUNCTION = "generate"

    # OUTPUT_NODE = False

    CATEGORY = "🐬 CyberDolphin"

    def validate_content(self, temperature: float, top_p: float = None) -> list[str]:
        errors_list = []
        if temperature is None and top_p is None:
            errors_list.append('Must contain a temperature or a top_p')
        if top_p < 0 or top_p > 1:
            errors_list.append('top_p must be a number between 0 and 1')
        if temperature < 0 or temperature > 2:
            errors_list.append(
                """Temperature should be a value between 0.0 and 2.0
                 - higher values like 0.8 will make the output more random,
                 lower values like 0.2 make it more focused and deterministic.
                 """)
        return errors_list

    def api_settings(self):
        openai_settings = load_settings()['openai']
        return openai_settings['api_base'], openai_settings['api_key'], openai_settings['organisation']

    def generate(self, model: str, system_prompt: str, user_prompt="",
                 temperature: float | None = None, top_p: float | None = None):
        errors = self.validate_content(temperature, top_p)
        if errors:
            error_report = "\n".join([e for e in errors])
            raise RuntimeError(f"There were problems with the parameters:\n{error_report}")
        else:

            system_content = system_prompt
            user_content = user_prompt
            if top_p == 0.0:
                openai.api_base, openai.api_key, openai.organization = self.api_settings()
                response = openai.ChatCompletion.create(
                    model=model,
                    temperature=temperature,
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": user_content}
                    ]
                )
            else:
                openai.api_base, openai.api_key, openai.organization = self.api_settings()
                response = openai.ChatCompletion.create(
                    model=model,
                    top_p=top_p,
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": user_content}
                    ]
                )

            return (f'{response.choices[0].message.content}',)
