# Lofi X Rain

## Repository
https://github.com/ZacharyHuerta/Zachary-Huerta-2305.0W1-Final-Project-Lofi-x-Rain.git

## Desciption
An animated and interactive program that showcases a study room with digital rain cascading outside of the room's window.
Cycling through music, room colors, and digital rain variations of your choice will help to create a relaxing virtual study space.

## Features
- Rain Cycling
  - Through using Pygames drawing tools, particle systems, and utilizing sprite animations the program will create rain visuals that can be cycled through.
- Music Cycling
  - Using Pygames mixer module the program can switch between lo-fi audio tracks loaded from local audio folder cycled through in order or randomly.
- Room Color Cycling
  - Cycling through room color themes by using pygame to apply color overlays using transparency layers / blitting.
- HUD
  - On screen overlay showing current rain styles, music playing, and room color using pygame for text display / blitting.

## Challenges
- Creating the room, planning layer order of background, furniture, window, and foreground while importing / positoning correctly with Pygame display.
- Building HUD that can manage all features displayed while not being intrusive, possibly animated too or interactive with buttons.
- Learning how to make a clean game loop that draws multiple independent layers without having performance issuses.
- Researching how to implement Pygames mixer module for playing audio and transitioning through music smoothly while displaying what is being played.
- Furthering my research on how to organize a Python project with multiple asset types and modules in VS Code so the codebase stays readable / 'debuggable' (LOL) as features are added.

## Outcomes
Ideal Outcomes
- A fully interactive Pygame window showcasing a relaxing study room with digital rain cascading in and out of view outside a window pane as a computer monitor has your desired music scrolling on its display.
  With buttons that are animated you can control the program through keyboard or mouse, cycling through desired rain, room color theme, and music. 

Minimal Viable Outcome:
- A Pygame window displaying what resembles a room, though maybe not as a cozy as desired, a digital rain still falls outside of the window. Still with a computer in the room displaying what music is be cycled through
  it just wont look as fancy of animation. A HUD is still displayed but not interactive through buttons, all cycling can be done through displayed keybindings shown in HUD. 

## Milestones

- Week1
- Create a static room scene that has a clearly defined space for the window to have the rain animation be seen.

- Week 2
- Implement rain animation loop and create new styles that can be cycled through with keyboard controls. Begin designing HUD layout, animation and Button class.

- Week 3
- Integrate music playback feature via Pygame mixer module and connect all cycling features together with animated HUD feedback / interactive buttons and polish overall presentation of program for submission. 
