# basic-particle simulation

Hello, World! I recently discovered a Python library called Taichi. It piqued my interest, so I spent a day experimenting with it and ended up making a very basic particle simulation.

The core philosophy of this short project was that the `engine.py` file, or henceforth simply the **Engine**, would be the **ultimate** source of truth. `main.py`, which contains the code responsible for rendering the particles, knows nothing about *why* a particle is at a particular position or *how* it got there. It simply takes the state of the simulation and renders it.

I think this is a great design pattern because it keeps the physics and rendering separate. We don't have to rely on camera tricks or manually move things around to make the simulation look correct. We can simply change the initial conditions, add more particles, or change the physics and *voila* — the renderer just reflects the new state of the simulation.

## So why Taichi?

Taichi is a Python-embedded language primarily written in C++. It is designed around high-performance computation and parallel programming, which makes it particularly useful for things like physics simulations and rendering where massive numbers of calculations need to be performed.

It still looks and feels like Python, but decorators are used to mark functions that should be passed to Taichi's compiler. Taichi can then compile these functions to run on different CPU/GPU backends.

This was particularly interesting to me because I could write the physics in a Python-like syntax while still taking advantage of parallel computation on the GPU.

## Problems
One major problem I encountered was that particles could pass directly through one another. This was initially surprising, but it exposed an important limitation of my model. I wanted the simulation to obey real physics rather than adding arbitrary collision detection, but I had only implemented the electrostatic force between point charges. Coulomb's law alone does not provide a mechanism that prevents two opposite point charges from occupying the same position.

This made me realise that before adding more forces, I need to decide exactly what physical system I am trying to model. I initially started with Coulomb's law simply because it was the first physical interaction that came to mind. If I want to model actual particles, however, I need a more complete physical model rather than expecting Coulomb's law by itself to reproduce the behaviour of real matter.

Another problem was the numerical integration method I initially used: Euler integration. In my implementation, I calculated the acceleration from the current force and assumed that acceleration remained constant over the entire timestep:

$$v_{t+\Delta t} = v_t + a_t \Delta t$$
$$x_{t+\Delta t} = x_t + v_t \Delta t$$

This is an approximation. In a system where forces change rapidly, such as two charged particles getting very close together, the acceleration can change dramatically during a single timestep. 
Euler integration therefore becomes increasingly inaccurate and can produce unstable behaviour.

This led me to investigate Verlet integration as an alternative numerical integration method (Not implemented yet).

## What's Next

My next step is to replace the current Euler integration with Verlet integration and compare the behaviour of the simulation. I want to investigate whether this improves the stability and energy conservation of the system, particularly when the particles get close together.

After that, I want to improve the physical model itself. Rather than adding artificial collision detection to prevent particles from passing through one another, I want to understand what physical interactions would actually produce this behaviour.

This means moving beyond simply implementing equations that I already know and learning more about the physics behind real particles. I plan to read introductory material on condensed matter physics and particle physics, and use what I learn to decide what level of physical modelling is appropriate for this project.

I am particularly interested in eventually exploring whether some aspects of quantum behaviour could be incorporated into the simulation. However, I don't want to force a quantum-mechanical model onto the project before I understand the physics well enough to justify it. 
For now, the goal is to build a solid classical simulation engine and use it as a foundation for experimenting with increasingly realistic physical models.
