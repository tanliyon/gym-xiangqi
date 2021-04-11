Examples
========

In this page, we provide some example usage of our Xiangqi environment.
Xiangqi environment has two main usage. First one is, of course, training 
the reinforcement learning agent, and the second one is running a game 
that you can play against your reinforcement learning agent.

Training
--------
If you are familiar working with OpenAI gym environment. Then, you can skip
this part since most of these will be something you already know.

Creating and running a Xiangqi environment is pretty simple. Let's get started
by creating and opening a Python script file. Then follow these steps:

1. Create a Xiangqi environment
This can be either done with :code:`gym.make()` or instantiating 
:code:`XiangQiEnv` object.

Using :code:`gym.make()`:

.. code-block:: python

   import gym
   env = gym.make('gym_xiangqi:xiangqi-v0')

Using :code:`XiangQiEnv` constructor:

.. code-block:: python

   from gym_xiangqi.envs import XiangQiEnv
   env = XiangQiEnv()

2. Create a training loop

Now, we will create a loop that will execute interactions between the agent 
and the environment. For this example, we will only loop one episode of Xiangqi game.
An episode is one full game of any reinforcement learning environment.

.. code-block:: python

   import time

   done = False
   while not done:
       time.sleep(1)
       env.render()
       action = env.action_space.sample()
       obs, reward, done, info = env.step(action)
   env.close()

Let's see what is happening in the loop, we have imported and added :code:`time.sleep(1)` 
to better obseve the game by adding a time delay. Then we create a flag called :code:`done` 
that will denote the terminating condition. So while done is :code:`False`, meaning current 
game is alive, 

we render our current game state

.. code-block:: python

   env.render()

we randomly sample an action

.. code-block:: python

   action = env.action_space.sample()

and feed that in to our environment

.. code-block:: python

   obs, reward, done, info = env.step(action)

As a result of calling :code:`env.step(action)`, we get four return values.

First return value is called the `observation` which represents current game board state 
after the given input action has been processed.

Second return value is called the `reward` which is the points received as a result of 
given input action. Note that, `reward` can be negative. For instance, this can happen if 
the given input action is an illegal piece action/move.

Third return value is called `done` which has the same functionality of :code:`done` 
variable we have initialized before the loop.

Last return value is called the `info` which is a dictionary that generally "contains 
auxiliary diagnostic information (helpful for debugging, and sometimes learning)". For our 
Xinagqi environment we only meaninful thing included in :code:`info` is whether the PyGame 
window has been closed with the window close button.

Finally at the end of the :code:`while` loop make sure to close the environment using 

.. code-block:: python

   env.close()

This will free up resources associated with the environment and exit the program gracefully.

These are just the basics of a Gym environment. Please also take a look at the 
`agent_v_agent_demo.py <https://github.com/tanliyon/gym-xiangqi/blob/main/gym_xiangqi/examples/agent_v_agent_demo.py>`_ 
file  located in our repository.
For more experience with Gym environments, please check out `OpenAI Gym repository <https://github.com/openai/gym>`_ 
and try out the environments implemented by OpenAI.

Game (Playing against your agent)
---------------------------------
Watching your agent interacting and playing within the environment is pretty cool, but  
the idea of battling against your agent is even more interesting. We will provide an example 
on how to play against your agent using our Xinagqi environment.

Let's build our understanding from the training example above. If you haven't already, we 
highly recommend you to read and try out the training example above first.

First add these import statements in addition to those added in the training example.

.. code-block:: python

   from gym_xiangqi.constants import RED, BLACK, PIECE_ID_TO_NAME, ALLY
   from gym_xiangqi.utils import action_space_to_move

Similar to the training code, we are going to first instantiate our Xiangqi environment, and 
create a loop to interact with the environment. This time our :code:`while` loop will look like 
this:

.. code-block:: python

   while not done:
       if env.turn == ALLY:
           obs, reward, done, info = env.step_user()

           if "exit" in info and info["exit"]:
               break

           piece, start, end = env.user_move_info
           piece = PIECE_ID_TO_NAME[piece]
       else:
           time.sleep(1)
           action = env.action_space.sample()
           obs, reward, done, info = env.step(action)


We have the same code for the :code:`else` block which executes when it is the enemy's turn 
but then now when it is an ally turn, we run 

.. code-block:: python

   obs, reward, done, info = env.step_user(action)

which has similar functionality as :code:`env.step()` but is designed for the users. Specifically, 
it allows users to input piece movements using mouse clicks on our GUI. As mentioned a little bit 
in the training example, the :code:`info` dictionary may carry information that tells users that 
the game window has been closed by the window close button. For debugging and observation purposes, 
we saved the user piece movement information as an object variable. We can add a few more lines 
from the code above to render the game and log some piece movements on our terminal window. The full 
:code:`while` loop will look like this:

.. code-block:: python

   while not done:
       if env.turn == ALLY:
           obs, reward, done, info = env.step_user()

           if "exit" in info and info["exit"]:
               break

           player = "You"
           piece, start, end = env.user_move_info
           piece = PIECE_ID_TO_NAME[piece]
       else:
           time.sleep(1)
           action = env.action_space.sample()
           obs, reward, done, info = env.step(action)

           player = "RL Agent"
           move = action_space_to_move(action)
           piece = PIECE_ID_TO_NAME[move[0]]
           start = move[1]
           end = move[2]

       env.render()
       round += 1
       print(f"Round: {round}")
       print(f"{player} made the move {piece} from {start} to {end}.")
       print(f"Reward: {reward}")
       print("================")
   env.close()

Most of this code is referenced from our `game_mode.py <https://github.com/tanliyon/gym-xiangqi/blob/main/gym_xiangqi/examples/game_mode.py>`_
file in our repository .
Please do also check it out. Thanks for the interest!