"""
Simple Phase II interactive text game.

This file wraps a generated crime story in a playable text interface. It can
use an LLM to convert any story text file into interactive plot points. If the
LLM is unavailable, it falls back to the built-in exemplar story.
"""

from dataclasses import dataclass, field
import argparse
import json
import re

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


@dataclass
class PlotPoint:
    title: str
    location: str
    clue: str
    required_terms: list[str]
    description: str


@dataclass
class GameState:
    plot_index: int = 0
    location: str = "Convention Center Alley"
    inventory: list[str] = field(default_factory=list)
    solved: bool = False
    failed: bool = False


class DramaManager:
    def __init__(self, plot_points, client=None):
        self.plot_points = plot_points
        self.client = client
        self.log = []

    def classify_action(self, action, state):
        if self.client:
            llm_classification = self.classify_action_with_llm(action, state)
            if llm_classification:
                return llm_classification

        action = action.lower()
        exceptional_terms = [
            "destroy",
            "burn",
            "throw away",
            "kill",
            "leave city",
            "ignore case",
            "arrest ethan",
            "arrest nadia",
            "bring isla",
            "open fire stair",
        ]
        if any(term in action for term in exceptional_terms):
            return "exceptional"

        current = self.plot_points[state.plot_index]
        if any(term in action for term in current.required_terms):
            return "constituent"

        helpful_terms = ["look", "search", "inspect", "ask", "talk", "go", "move", "call"]
        if any(term in action for term in helpful_terms):
            return "consistent"

        return "consistent"

    def classify_action_with_llm(self, action, state):
        current = self.plot_points[state.plot_index]
        try:
            response = self.client.responses.create(
                model="gpt-5-nano",
                input=[
                    {
                        "role": "system",
                        "content": (
                            "You classify player actions in an interactive crime "
                            "story. Return only one word: constituent, consistent, "
                            "or exceptional."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Current plot point: {current.title}\n"
                            f"Location: {current.location}\n"
                            f"Needed clue: {current.clue}\n"
                            f"Helpful terms: {current.required_terms}\n"
                            f"Player action: {action}\n\n"
                            "Classify as constituent if the action finds or pursues "
                            "the needed clue, consistent if it is harmless but does "
                            "not advance the plot, and exceptional if it would break "
                            "the story or make solving the case impossible."
                        ),
                    },
                ],
            )
            classification = response.output_text.strip().lower()
            if "exceptional" in classification:
                return "exceptional"
            if "constituent" in classification:
                return "constituent"
            if "consistent" in classification:
                return "consistent"
        except Exception:
            return None
        return None

    def respond(self, action, state):
        classification = self.classify_action(action, state)

        if classification == "exceptional":
            message = self.handle_exception(action, state)
        elif classification == "constituent":
            message = self.advance_story(state)
        else:
            message = self.give_hint(state)

        self.log.append((action, classification, message))
        return classification, message

    def handle_exception(self, action, state):
        current = self.plot_points[state.plot_index]
        if "open fire stair" in action.lower():
            state.failed = True
            return (
                "DM ACTION: The drama manager allows the mistake. The fire stair "
                "was the trap Aria warned about, and the rescue path is lost."
            )

        return (
            "DM ACTION: Accommodation. That action would break an active story "
            f"condition, so the drama manager blocks it and redirects you toward "
            f"{current.location}."
        )

    def advance_story(self, state):
        current = self.plot_points[state.plot_index]
        state.location = current.location
        if current.clue not in state.inventory:
            state.inventory.append(current.clue)

        response = (
            f"DM ACTION: Constituent action accepted.\n"
            f"{current.description}\n"
            f"New clue: {current.clue}"
        )

        state.plot_index += 1
        if state.plot_index >= len(self.plot_points):
            state.solved = True
            response += "\nMara rescues Aria and identifies Malik as the kidnapper."
        return response

    def give_hint(self, state):
        current = self.plot_points[state.plot_index]
        return (
            "DM ACTION: Hint. Your action does not break the story, but it does "
            f"not uncover the next key clue. Focus on {current.location}; try to "
            f"investigate {current.required_terms[0]}."
        )


class CrimeStoryGame:
    def __init__(self, story_path=None, use_llm=False):
        self.client = create_client() if use_llm else None
        self.plot_points = self.load_plot_points(story_path)
        self.state = GameState()
        self.state.location = self.plot_points[0].location
        self.dm = DramaManager(self.plot_points, client=self.client)

    def load_plot_points(self, story_path):
        if story_path and self.client:
            try:
                with open(story_path, "r", encoding="utf-8") as story_file:
                    story_text = story_file.read()
                plot_points = build_plot_points_with_llm(self.client, story_text)
                if plot_points:
                    print(f"Loaded interactive plot from {story_path} using the LLM.")
                    return plot_points
            except Exception as error:
                print(f"Could not build LLM plot points: {error}")

        if story_path and not self.client:
            print("No OpenAI client available. Using built-in exemplar plot points.")
        return default_plot_points()

    def print_status(self):
        if self.state.solved or self.state.failed:
            return
        current = self.plot_points[self.state.plot_index]
        print("\nCurrent location:", self.state.location)
        print("Next lead:", current.title)
        print("Inventory:", ", ".join(self.state.inventory) or "none")

    def apply_action(self, action):
        classification, message = self.dm.respond(action, self.state)
        print("\nUSER ACTION:", action)
        print("CLASSIFICATION:", classification)
        print(message)

    def play(self):
        print("Crime Story Phase II Game")
        print("You are Detective Mara Vance. Type actions, or type quit.")
        while not self.state.solved and not self.state.failed:
            self.print_status()
            action = input("\nWhat do you do? ").strip()
            if action.lower() == "quit":
                break
            if not action:
                continue
            self.apply_action(action)

        self.print_ending()

    def run_demo(self):
        demo_actions = [
            "inspect the camera bag and recover the usb",
            "search Basement 3 for the second shelf tag",
            "go to the hotel and inspect the hard case framing Nadia",
            "check the donor ramp parking list and CCTV",
            "protect Isla at the apartment and collect the black fiber",
            "use the freight Car 2 machine room records to find Malik",
        ]
        print("Crime Story Phase II Demo Run")
        for action in demo_actions:
            self.print_status()
            self.apply_action(action)
            if self.state.solved or self.state.failed:
                break
        self.print_ending()

    def print_ending(self):
        print("\nDrama Manager Log")
        for index, (action, classification, message) in enumerate(self.dm.log, start=1):
            short_message = message.split("\n")[0]
            print(f"{index}. {classification}: {action} -> {short_message}")

        if self.state.solved:
            print("\nResult: SUCCESS. Aria is rescued and Malik is exposed.")
        elif self.state.failed:
            print("\nResult: FAILURE. The story was derailed by an exceptional action.")
        else:
            print("\nResult: STOPPED. The player quit before the ending.")


def main():
    parser = argparse.ArgumentParser(description="Play the Phase II crime story game.")
    parser.add_argument("--demo", action="store_true", help="Run a scripted demo to completion.")
    parser.add_argument("--story", help="Path to a generated story text file.")
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Use the OpenAI API to build plot points and classify actions.",
    )
    args = parser.parse_args()

    use_llm = args.llm or args.story is not None
    game = CrimeStoryGame(story_path=args.story, use_llm=use_llm)
    if args.demo:
        game.run_demo()
    else:
        game.play()


def default_plot_points():
    return [
        PlotPoint(
            "Alley Evidence",
            "Convention Center Alley",
            "USB drive and smudged security badge",
            ["usb", "badge", "alley", "camera bag"],
            "You recover the USB drive and notice the staged guard badge.",
        ),
        PlotPoint(
            "Basement 3",
            "Basement 3",
            "B3-COLD shelf tag",
            ["basement", "shelf", "b3", "access log"],
            "You follow the maintenance trail to Basement 3 and find the shelf tag.",
        ),
        PlotPoint(
            "Hotel Red Herring",
            "Downtown Hotel",
            "Nadia framing package",
            ["hotel", "nadia", "hard case", "service elevator"],
            "The evidence points at Nadia, but the drama manager marks it as a red herring.",
        ),
        PlotPoint(
            "Donor Ramp",
            "Private Donor Ramp",
            "delayed CCTV feed and valet list",
            ["donor", "ramp", "parking", "valet", "cctv"],
            "You find the donor ramp package and confirm the kidnapper is steering you.",
        ),
        PlotPoint(
            "Protect Isla",
            "Aria's Apartment",
            "black uniform fiber",
            ["isla", "apartment", "nursery", "fiber"],
            "You protect Isla instead of bringing her to the trap, preserving the rescue path.",
        ),
        PlotPoint(
            "Freight System",
            "Freight Machine Room",
            "Car 2 maintenance log",
            ["freight", "car 2", "machine", "elevator", "malik"],
            "You use the freight records to locate Aria and expose Malik.",
        ),
    ]


def create_client():
    if OpenAI is None:
        return None
    api_key = load_api_key()
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def load_api_key():
    try:
        with open("story_generation.py", "r", encoding="utf-8") as source_file:
            source = source_file.read()
        match = re.search(r'api_key\s*=\s*"([^"]+)"', source)
        if match:
            return match.group(1)
    except OSError:
        return None
    return None


def build_plot_points_with_llm(client, story_text):
    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {
                "role": "system",
                "content": (
                    "You turn generated crime stories into simple interactive "
                    "text-game plot points. Return valid JSON only."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Read this crime story and extract 6 to 10 playable plot "
                    "points for a detective text game. Each plot point must have "
                    "these fields: title, location, clue, required_terms, "
                    "description. required_terms must be a list of 3 to 6 short "
                    "lowercase strings a user might type to pursue that clue. "
                    "Return a JSON list and no other text.\n\n"
                    f"STORY:\n{story_text[:12000]}"
                ),
            },
        ],
    )
    data = parse_json_response(response.output_text)
    plot_points = []
    for item in data:
        plot_points.append(
            PlotPoint(
                title=str(item["title"]),
                location=str(item["location"]),
                clue=str(item["clue"]),
                required_terms=[str(term).lower() for term in item["required_terms"]],
                description=str(item["description"]),
            )
        )
    return plot_points


def parse_json_response(text):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()
    return json.loads(cleaned)


if __name__ == "__main__":
    main()
