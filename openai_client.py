import openai

from custom_nodes.cyberdolphin.settings import api_settings


class OpenAiClient:
    @staticmethod
    def complete(key, model, temperature, top_p, system_content, user_content):
        if top_p == 0.0:
            top_p = 0.001

        openai.api_base, openai.api_key, openai.organization = api_settings(key)
        response = openai.ChatCompletion.create(
            model=model,
            temperature=temperature,
            top_p=top_p,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ]
        )
        return response
