"""
Simple Phase II interactive text game.

This file wraps one generated crime story in a playable text interface. The
player acts as Detective Mara Vance. The drama manager classifies each typed
action as constituent, consistent, or exceptional, then advances, hints, or
blocks progress.
"""

from dataclasses import dataclass, field
import argparse


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
    def __init__(self, plot_points):
        self.plot_points = plot_points
        self.log = []

    def classify_action(self, action, state):
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
    def __init__(self):
        self.plot_points = [
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
        self.state = GameState()
        self.dm = DramaManager(self.plot_points)

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
    args = parser.parse_args()

    game = CrimeStoryGame()
    if args.demo:
        game.run_demo()
    else:
        game.play()


if __name__ == "__main__":
    main()
