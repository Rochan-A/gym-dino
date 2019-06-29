# OpenAI Gym Environment of the Chrome T-Rex Game

A pygame based port of the Chrome T-Rex Game as an OpenAI Gym Environment.

## Important info

You can change the FPS of the game by adjusting the env.FPS value. By default, it is at 60.

`Action Space = [0, 1, 2]
`

`
0 : No action
`

`
1 : Duck
`

`
2 : Jump
`

You can install this from PYPI:

```
pip3 install gym-dino
```

You can import it as:

```
import gym_dino
```

### Small backstory

I am currently working on some reinforcement learning research problems and really wanted a simple yet effective environment to train an agent on. I realised that the Chrome game ain't bad at all especially in this scenario.

So have fun, any help to further develop on this is welcome.

Right now, only ```render```, ```step```, ```reset``` and ```close``` function have been implemented.

---

Special thanks to [Shivam Shekar's](https://github.com/shivamshekhar/Chrome-T-Rex-Rush) implementation of the original game using pygame.
