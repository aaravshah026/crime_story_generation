from openai import OpenAI

class StoryModel:
    def __init__(self, api_key):
        # OpenAI Model
        self.client = OpenAI(api_key=api_key)

        # Current story elements
        self.story = []

        # Current story retelling
        self.retelling = None
    
    # function that updates the story version using the generated new events
    def update(self, new_events):
        self.story.append(new_events)
    
    # function that retells the story after everything has been generated
    def retell(self):
        response = self.client.responses.create(
            model="gpt-5.2",
            input=[
                {
                    "role": "system",
                    "content": "You are generating a story for a hostage kidnapping mystery with a 24 hour countdown. Preliminary instructions to obey for the entire conversation, without fail: - do not include lengthy explanations unless otherwise asked for - no expressing your emotions, keep the conversation factual and concise."
                },
                {
                    "role": "user",
                    "content": f"Given the events {self.story}, rewrite the entire story to make it flow clearly. This should read like an actual novel with long paragraphs. Do not include any additional details not in the events already. The countdown must be noticed in the actual story (not as headers)."
                }
            ]
        )
        self.retelling = response.output_text