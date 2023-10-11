import openai
from .settings import load_settings

all_settings = load_settings()
prompt_templates = all_settings['prompt_templates']
openai_settings = all_settings['openai_compatible']
openai.api_base = openai_settings['api_base']
openai.api_key = openai_settings['api_key']
openai.organization = openai_settings['organisation']
default_user_prompt = all_settings['example_user_prompt']


class CyberdolphinOpenAICompatible:
    the_settings = None
    def api_settings(self):
        openai_settings = load_settings()['openai_compatible']
        return openai_settings['api_base'], openai_settings['api_key'], openai_settings['organisation']

    @classmethod
    def INPUT_TYPES(s):
        openai.api_key = openai_settings['api_key']
        openai.organization = openai_settings['organisation']
        openai.api_base = openai_settings['api_base']
        available_models = [m["id"] for m in openai.Model.list()['data']]
        return {
            "required": {
                "api_base": ("STRING", {
                    "default": openai_settings['api_base']
                }),
                "prompt_template": ([t for t in prompt_templates], {
                    "default": 'default'
                }),
                "model": (available_models, {
                    "default": available_models[0]}),
                "user_prompt": ("STRING", {
                    "multiline": True,
                    "default": default_user_prompt
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
            errors_list.append("top_p must be a number between 0 and 1")
        if temperature < 0 or temperature > 2:
            errors_list.append(
                """Temperature should be a value between 0.0 and 2.0
                 - higher values like 0.8 will make the output more random, lower values like 0.2 make it more focused and deterministic.
                 """)
        return errors_list

    def generate(self, api_base: str, prompt_template: str, model: str, temperature: float | None = None,
                 top_p: float | None = None, user_prompt=""):
        errors = self.validate_content(temperature, top_p)
        if top_p == 0.0:
            top_p = None
        if errors:
            error_report = "\n".join([e for e in errors])
            raise RuntimeError(f"There were problems with the parameters:\n{error_report}")

        else:
            this_prompt = load_settings()['prompt_templates'][prompt_template]
            system_content = this_prompt['system']
            user_content = f"{this_prompt['prefix']} {user_prompt} {this_prompt['suffix']}"

            openai.api_base, openai.api_key, openai.organization = self.api_settings()

            # openai_settings = load_settings()['openai_compatible']
            # openai.api_base = openai_settings['api_base']
            # openai.api_key = openai_settings['api_key']
            # openai.organization = openai_settings['organisation']
            if top_p is None:
                response = openai.ChatCompletion.create(
                    model=model,
                    temperature=temperature,
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": user_content}
                    ]
                )
            else:
                response = openai.ChatCompletion.create(
                    model=model,
                    top_p=top_p,
                    messages=[
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": user_content}
                    ]
                )

            return (f'{response.choices[0].message.content}',)
