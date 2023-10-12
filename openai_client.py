import openai

from custom_nodes.cyberdolphin.settings import api_settings


def validation(temperature: float, top_p: float = None) -> list[str]:
    errors_list = []
    if temperature is None and top_p is None:
        errors_list.append('Must contain a temperature or a top_p')
    if top_p < 0 or top_p > 1:
        errors_list.append('top_p must be a number between 0 and 1')
    if temperature < 0 or temperature > 2:
        errors_list.append(
            """Temperature should be a value between 0.0 and 2.0
             - openai says higher values like 0.8 will make the output more random,
             lower values like 0.2 make it more focused and deterministic.
             """)
    return errors_list


class OpenAiClient:

    @staticmethod
    def complete(key: str, model: str, temperature: float, top_p: float, system_content: str, user_content: str):
        errors = validation(temperature, top_p)
        if errors:
            error_report = "\n".join([e for e in errors])
            raise RuntimeError(f"There were problems with the parameters:\n{error_report}")

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
