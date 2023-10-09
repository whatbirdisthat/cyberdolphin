from gradio_client import Client

from .settings import load_settings


class CyberDolphinGradioApi:

    @classmethod
    def INPUT_TYPES(s):
        """
            Return a dictionary which contains config for all input fields.
            Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT".
            Input types "INT", "STRING" or "FLOAT" are special values for fields on the node.
            The type can be a list for selection.

            Returns: `dict`:
                - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property `required`
                - Value input_fields (`dict`): Contains input fields config:
                    * Key field_name (`string`): Name of a entry-point method's argument
                    * Value field_config (`tuple`):
                        + First value is a string indicate the type of field or a list for selection.
                        + Second value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "text": ("STRING", {
                    "default": '',
                    "multiline": True,
                    "forceInput": True
                }),
                "llm_prompt": ([p for p in load_settings()['prompts']], "STRING"),
            },
        }

    RETURN_TYPES = ("STRING",)
    # RETURN_NAMES = ("image_output_name",)

    FUNCTION = "generate"

    # OUTPUT_NODE = False

    CATEGORY = "🐬 CyberDolphin"

    def generate(self, text="", llm_prompt: str = "default_prompt"):
        settings = load_settings()
        client_src = settings['gradio_chat_interface']['src']
        client = Client(client_src)
        prompt_prefix = settings['prompts'][llm_prompt]['prefix']
        prompt_suffix = settings['prompts'][llm_prompt]['suffix']

        prompt = f'{prompt_prefix} {text} {prompt_suffix}'
        # prompt = f'{self.PREFIX_PROMPT}{string_field}{self.SUFFIX_PROMPT}'
        result = client.predict(prompt, api_name="/chat")
        response = result
        return (f'{response}',)


if __name__ == "__main__":
    print("Hello there.")
