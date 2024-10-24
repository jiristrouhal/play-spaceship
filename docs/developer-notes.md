# Zeroth version - simple vertical landing using calculator

This version can be used to simply land the spaceship based on its current state, without an ability to tell the ship where to land.

However, the aim it to use the base of the agent and use it even for systems, where the governing rules are not known (complicated physical systems, social interactions etc.)

A use of a specialized calculator is thus undesired here. The system should learn the rules by itself. The advantage here is the ability to run the game over and over wihout any penalty, so the agent is allowed to "learn".


# First version - make the agent learn the rules

The goal of the agent is not only to land the rocket, but to learn the rules first, including the rocket behavior. The agent should be able to recognize, when it is ready to try to land the rocket and remember the rules for the next time.

