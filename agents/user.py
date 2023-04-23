from openai import ChatCompletion


class UserAgent:
    """
    Agent that acts as a user and performs actions.
    """

    def __init__(self, persona_prompt: str, model: str = "gpt-4", max_retries=3):
        """
        Initialize the user agent.
        """
        self.persona_prompt = persona_prompt
        self.model = model
        self.max_retries = max_retries
        self.persona = None

        self.MESSAGES = [
            {
                "role": "system",
                "content": "You are BrowseGPT, a browsing assistant designed to help developers test their web apps by simulating how different personas might interact with it. Read the person prompt below and imagine you are the persona described. Then, follow the intructions to read the state of the website, perform actions, and provide explanations for your actions, as the persona would.",
            },
            {"role": "user", "content": persona_prompt},
        ]

    def _chat_completion(self, message, temperature=0.1):
        if isinstance(message, list):
            self.MESSAGES.extend(message)
        else:
            self.MESSAGES.append(message)

        response = ChatCompletion.create(
            model=self.model,
            messages=self.MESSAGES,
            temperature=temperature,
        )["choices"][0]["message"]["content"]

        self.MESSAGES.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        return response

    def select_action(self, action_space: dict):
        """
        Select an action from the action space, based on the user's persona and past memories.
        """

        action_prompt = f"""
            The following is a dictionary of possible actions you can take on this website, represented as a Python dictionary:\n\n

            {action_space}\n\n

            Read the actions carefully, and imagine you are the persona described above.
            Pick *one* action that you would take, which most aligns what the persona would do when visiting the website.
            Please return only the key to the python dictionary that corresponds to the action you would like to take.
            Do not return any other text.
            """

        action_str = self._chat_completion({"role": "user", "content": action_prompt})

        print(f"Action selected: {action_str}")

        max_retries = self.max_retries
        while action_str not in action_space and max_retries > 0:
            retry_prompt = f"""
                The action you selected is not a valid key to the dictionary. Please try again. You have {max_retries} retries left.\n\n

                Here is the Python dictionary representing the possible actions:\n\n

                {action_space}\n\n
                """
            action_str = self._chat_completion(
                [
                    {"role": "user", "content": retry_prompt},
                    {
                        "role": "system",
                        "content": "Remember, you should only return a valid key to the dictionary. **IMPORTANT:** Be very terse. Do not return any other text!",
                    },
                ]
            )

            max_retries -= 1

            print(f"Action selected: {action_str}")

        if max_retries == 0:
            raise Exception(
                "User Agent did not select a valid action after 3 retries. Please try again."
            )

        return action_str

    def get_explantion(self):
        explanation_prompt = f"""
            Please explain why you chose this action. Imagine you are the persona described above. What was your intent as the persona? What were you trying to acomplish with this action?
            """

        explanation_str = self._chat_completion(
            {"role": "user", "content": explanation_prompt}, temperature=0.8
        )

        return explanation_str

    def update_state(self, state: dict):
        """
        Pass the updated state of the website as a Update the user's persona based on the new state.
        """

        state_prompt = f"""
            The following is a python dictionary representing the current state of the website, after performing the actions above:\n\n

            {state}\n\n

            Read the state carefully, and imagine you are the persona described above. Start thinking about what action you would take next, based on the current state of the website. Write your initial thoughts below.
        """

        ack_response = self._chat_completion({"role": "user", "content": state_prompt})

        return state
