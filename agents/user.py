from openai import ChatCompletion


class UserAgent:
    """
    Agent that acts as a user and performs actions.
    """

    def __init__(self, persona_prompt: str, model: str = "gpt-4"):
        """
        Initialize the user agent.
        """
        self.persona_prompt = persona_prompt
        self.persona = None

        self.MESSAGES = [
            {"role": "system", "content": "."},
        ]

    def _chat_completion(self):
        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {
                    "role": "assistant",
                    "content": "The Los Angeles Dodgers won the World Series in 2020.",
                },
                {"role": "user", "content": "Where was it played?"},
            ],
        )

        return response["choices"][0]["message"]["content"]

    def select_action(self, action_space: dict):
        """
        Select an action from the action space, based on the user's persona and past memories.
        """

        # Get the user's persona
        if not self.persona:
            self.persona = self._chat_completion()

        # Select an action
        action = "click"

        return action
