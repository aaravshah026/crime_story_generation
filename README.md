# crime_story_generation

Welcome to Group Hot Dogs' story generation project.

## Instructions

1. If you do not have the OpenAI library installed, create a virtual environment and run:

```bash
pip install -r requirements.txt
```

2. To run the original story generator (typical runtime - 20 minutes, cost - $1):

```bash
python3 story_generation.py
```

3. To run the Phase II interactive text game (typical runtime - 1-5 minutes, cost - <$1):

```bash
python3 phase2_game.py
```

4. To run the Phase II demo without typing actions:

```bash
python3 phase2_game.py --demo
```

5. To make a different generated story interactive, pass in a story text file. This uses the OpenAI API to extract interactive plot points and classify player actions:

```bash
python3 phase2_game.py --story exemplar_story_1.txt
```

Note: if the API key does not work, replace the key in `story_generation.py` with your own key.

## Documentation

### Team Name

Group Hot Dogs

### System Name

Crime Story Generation: Phase II Interactive Detective Game

### Project Template

Intervention and Accommodation.

The user plays as the detective. The system classifies each user action as:

- constituent: the action advances the intended story
- consistent: the action is allowed but does not advance the main plot
- exceptional: the action threatens to break the story

When an exceptional action happens, the drama manager either blocks the action and redirects the player, or allows failure if the player triggers a major trap.

### How The Code Is Organized

- `story_generation.py`: runs the original story generation pipeline
- `world_generation.py`: creates the detective, victim, suspects, clues, and perpetrator
- `world_model.py`: generates plot events and checks consistency
- `story_model.py`: stores generated events and retells the final story
- `phase2_game.py`: playable Phase II text game and drama manager. It can use the LLM to convert a story text file into interactive plot points.
- `exemplar_story_1.txt` and `exemplar_story_2.txt`: generated example stories used for testing and demonstration

### Runtime And Cost

The original story generator usually takes 10-20 minutes because it calls the OpenAI API many times. It may cost money depending on the API account and model pricing.

The Phase II demo runs immediately. The `--demo` mode does not call the API, so it has no API cost.

Running `phase2_game.py --story some_story.txt` calls the OpenAI API to build interactive plot points from that story and to classify user actions during play. This adds API cost, but it allows the Phase II layer to work on a newly generated story instead of only one hardcoded story.

### Walkthrough 1: Successful Run

USER ACTION: inspect the camera bag and recover the usb  
DRAMA MANAGER ACTION: classifies the action as constituent and gives the USB clue.

USER ACTION: search Basement 3 for the second shelf tag  
DRAMA MANAGER ACTION: classifies the action as constituent and advances to the Basement 3 clue.

USER ACTION: go to the hotel and inspect the hard case framing Nadia  
DRAMA MANAGER ACTION: classifies the action as constituent and marks Nadia as a red herring.

USER ACTION: check the donor ramp parking list and CCTV  
DRAMA MANAGER ACTION: classifies the action as constituent and shows that the kidnapper is steering the detective.

USER ACTION: protect Isla at the apartment and collect the black fiber  
DRAMA MANAGER ACTION: classifies the action as constituent and preserves the rescue path.

USER ACTION: use the freight Car 2 machine room records to find Malik  
DRAMA MANAGER ACTION: classifies the action as constituent and completes the rescue.

### Walkthrough 2: Exceptional Action

USER ACTION: destroy the usb evidence
DRAMA MANAGER ACTION: Accommodation. That action would break an active story condition, so the drama manager blocks it and redirects you toward Convention Center Alley.

### Walkthrough 3: AI System Responding to the Player to Change the Story (Template 1)

USER ACTION: open fire stair door  
DRAMA MANAGER ACTION: classifies the action as exceptional. This was the trap Aria warned about, so the story fails.

### Architecture Diagram

<img width="960" height="502" alt="Image" src="https://github.com/user-attachments/assets/76037b34-d970-4f88-923f-24d4d082f7d3" />

## Videos

### Proposal Video

https://youtu.be/C6L9NY5Koi8
