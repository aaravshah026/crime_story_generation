from openai import OpenAI

class WorldModel():
    def __init__(self, world, api_key):
        # OpenAI Model
        self.client = OpenAI(api_key=api_key)

        # Hidden crime plan details stored in the world model
        self.world = world

        # Current knowledge graph
        self.graph = []

        # Red herring count
        self.red_herrings = 0

        # Kidnapper interference event count
        self.kie = False
    
    # function that generates a new plot event
    def generate_plot_event(self, current_iteration, total_iterations):
        response = self.client.responses.create(
            model="gpt-5.2",
            input=[
                {
                    "role": "system",
                    "content": "You are generating a story for a hostage kidnapping mystery with a 24 hour countdown. Preliminary instructions to obey for the entire conversation, without fail: - do not include lengthy explanations unless otherwise asked for - no expressing your emotions, keep the conversation factual and concise."
                },
                {
                    "role": "user",
                    "content": f"The name of the detective is {self.world.detective}. The name and backstory of the victim is {self.world.victim}. The suspects are {self.world.suspects}. The clues at the crime scene are {self.world.clues}. The perpetrator and their reasoning are {self.world.perpetrator}. The things that the detective knows in the actual story are {self.graph}."
                },
                {
                    "role": "user",
                    "content": f"We are currently at plot point {current_iteration} out of {total_iterations}. Make sure that the story is complete by the end of the last iteration. Generate a new plot event for the story. Keep in mind that we need three red herrings (we have {self.red_herrings}) and we need a kidnapper interference event (currently {self.kie})."
                }
            ]
        )
        return response.output_text

    # function that checks to see if new events are consistent with world model
    def consistency_check(self, new_events):
        response = self.client.responses.create(
            model="gpt-5.2",
            input=[
                {
                    "role": "system",
                    "content": "You are generating a story for a hostage kidnapping mystery with a 24 hour countdown. Preliminary instructions to obey for the entire conversation, without fail: - do not include lengthy explanations unless otherwise asked for - no expressing your emotions, keep the conversation factual and concise."
                },
                {
                    "role": "user",
                    "content": f"The name of the detective is {self.world.detective}. The name and backstory of the victim is {self.world.victim}. The suspects are {self.world.suspects}. The clues at the crime scene are {self.world.clues}. The perpetrator and their reasoning are {self.world.perpetrator}. The things that the detective knows in the actual story are {self.graph}."
                },
                {
                    "role": "user",
                    "content": f"Check if the events in {new_events} are consistent with the hidden story and the detective's current knowledge. If they are, only say \"true\", otherwise tell me what the inconsistencies are in 1-2 sentences."
                }
            ]
        )
        consistency = True if "true" in response.output_text.lower() else False
        return consistency, response.output_text
    
    # function that updates the knowledge graph and associated counters
    def update(self, new_events):
        response = self.client.responses.create(
            model="gpt-5.2",
            input=[
                {
                    "role": "system",
                    "content": "You are generating a story for a hostage kidnapping mystery with a 24 hour countdown. Preliminary instructions to obey for the entire conversation, without fail: - do not include lengthy explanations unless otherwise asked for - no expressing your emotions, keep the conversation factual and concise."
                },
                {
                    "role": "user",
                    "content": f"The hidden story (the events that actually happen) are {self.world}. The things that the detective knows in the actual story are {self.graph}"
                },
                {
                    "role": "user",
                    "content": f"Create a new list of things the detective knows after the events in {new_events}."
                }
            ]
        )
        self.graph = response.output_text
        response2 = self.client.responses.create(
            model="gpt-5-nano",
            input=[
                {
                    "role": "system",
                    "content": "You are generating a story for a hostage kidnapping mystery with a 24 hour countdown. Preliminary instructions to obey for the entire conversation, without fail: - do not include lengthy explanations unless otherwise asked for - no expressing your emotions, keep the conversation factual and concise."
                },
                {
                    "role": "user",
                    "content": f"Do the events in {new_events} involve a red herring or a kidnapper interference event? If it involves a red herring, output \"red herring\". If it involves a kidnapper interference event, output \"kidnapper interference event\". IF there are none, output \"None\"."
                }
            ]
        )
        if "red herring" in response2.output_text.lower():
            self.red_herrings += 1
        if "kidnapper interference event" in response2.output_text.lower():
            self.kie = True
    

