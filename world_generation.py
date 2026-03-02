from openai import OpenAI

class World:
    def __init__(self, api_key):
        # OpenAI Model
        self.client = OpenAI(api_key=api_key)

        # creates the name for the protagonist
        self.detective = self.generate_detective()

        # creates the victime & their backstory
        self.victim = self.generate_victim()

        # creates a list of four suspects -- includes mean, motive, and opportunity reasoning for each
        self.suspects = self.generate_suspects()

        # creates a list of clues at the crime scene for the detective to use to catch the kidnapper
        self.clues = self.generate_clues()

        # decides the perpetrator, along with their actions that led them to commit the kidnapping
        self.perpetrator = self.generate_perpetrator()
    
    # function that generates the name of the detective (protagonist).
    def generate_detective(self):
        response = self.client.responses.create(
            model="gpt-5-nano",
            input=[
                {
                    "role": "system",
                    "content": "You are generating a story for a hostage kidnapping mystery with a 24 hour countdown. Preliminary instructions to obey for the entire conversation, without fail: - do not include lengthy explanations unless otherwise asked for - no expressing your emotions, keep the conversation factual and concise."
                },
                {
                    "role": "user",
                    "content": "Generate a realistic name for the detective. One name only."
                }
            ]
        )
        return response.output_text

    # function that generates the kidnapping victim and their backstory.
    def generate_victim(self):
        response = self.client.responses.create(
            model="gpt-5-nano",
            input=[
                {
                    "role": "system",
                    "content": "You are generating a story for a hostage kidnapping mystery with a 24 hour countdown. Preliminary instructions to obey for the entire conversation, without fail: - do not include lengthy explanations unless otherwise asked for - no expressing your emotions, keep the conversation factual and concise."
                },
                {
                    "role": "user",
                    "content": "Generate a realistic name for the kidnapping victime, along with a plausible backstory. One name and backstory only."
                }
            ]
        )
        return response.output_text

    # function that generates four suspects and their backstories, along with why they are connected to the victim, their motivation, and their alibis.
    def generate_suspects(self):
        response1 = self.client.responses.create(
            model="gpt-5-nano",
            input=[
                {
                    "role": "system",
                    "content": "You are generating a story for a hostage kidnapping mystery with a 24 hour countdown. Preliminary instructions to obey for the entire conversation, without fail: - do not include lengthy explanations unless otherwise asked for - no expressing your emotions, keep the conversation factual and concise."
                },
                {
                    "role": "user",
                    "content": "Generate realistic names for four suspects. One name only per suspect."
                }
            ]
        )
        names = response1.output_text
        response2 = self.client.responses.create(
            model="gpt-5-nano",
            input=[
                {
                    "role": "system",
                    "content": "You are generating a story for a hostage kidnapping mystery with a 24 hour countdown. Preliminary instructions to obey for the entire conversation, without fail: - do not include lengthy explanations unless otherwise asked for - no expressing your emotions, keep the conversation factual and concise."
                },
                {
                    "role": "user",
                    "content": f"The suspects' names are {names}. The victim's name and backstory are {self.victim}."
                },
                {
                    "role": "user",
                    "content": "For each suspect, provide: motive (1-2 sentences), connection to the victim, alibi for the last 24 hours. Return as a bullet list per suspect."
                }
            ]
        )
        return response2.output_text
    
    # function that generates 5 or more clues at the crime scene.
    def generate_clues(self):
        response = self.client.responses.create(
            model="gpt-5-nano",
            input=[
                {
                    "role": "system",
                    "content": "You are generating a story for a hostage kidnapping mystery with a 24 hour countdown. Preliminary instructions to obey for the entire conversation, without fail: - do not include lengthy explanations unless otherwise asked for - no expressing your emotions, keep the conversation factual and concise."
                },
                {
                    "role": "user",
                    "content": f"The victim's name and backstory are {self.victim}. The suspects names and backstories are {self.suspects}."
                },
                {
                    "role": "user",
                    "content": "Generate a realistic description for where the kidnapping took place and what clues (at least 5) were left behind."
                }
            ]
        )
        return response.output_text
    
    # function that decides the perpetrator, along with what actually happened when the crime took place.
    def generate_perpetrator(self):
        response = self.client.responses.create(
            model="gpt-5-nano",
            input=[
                {
                    "role": "system",
                    "content": "You are generating a story for a hostage kidnapping mystery with a 24 hour countdown. Preliminary instructions to obey for the entire conversation, without fail: - do not include lengthy explanations unless otherwise asked for - no expressing your emotions, keep the conversation factual and concise."
                },
                {
                    "role": "user",
                    "content": f"The victim's name and backstory are {self.victim}. The suspects names and backstories are {self.suspects}. The clues at the crime scene are {self.clues}."
                },
                {
                    "role": "user",
                    "content": "Decide who committed the crime from the suspects, along with what actually happened at the crime scene. Only pick one person."
                }
            ]
        )
        return response.output_text
    