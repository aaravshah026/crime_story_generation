# RUN THIS FILE TO GENERATE THE CRIME STORY!
from openai import OpenAI
from story_model import StoryModel
from world_generation import World
from world_model import WorldModel
api_key = "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"
num_plot_points = 15

# Generate world, world model, and story model objects
world = World(api_key=api_key)
world_model = WorldModel(world, api_key=api_key)
story_model = StoryModel(api_key=api_key)

# Generate the required number of plot points
for i in range(1, num_plot_points + 1):
    print(f"Iteration {i} beginning")
    
    # Generate events in the plot point and check for consistency
    new_events = world_model.generate_plot_event(i, num_plot_points)
    while not world_model.consistency_check(new_events)[0]:
        print(f"Inconsistency: {world_model.consistency_check(new_events)[1]}")
        new_events = world_model.generate_plot_event(i, num_plot_points)
    print(f"Iteration {i} plot point generated")

    # Update the world model and story model with the new consistent plot point
    world_model.update(new_events)
    story_model.update(new_events)

# Retell the story to polish it
story_model.retell()
print(story_model.retelling)