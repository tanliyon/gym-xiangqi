GUI
===

Users can observe the training and game progress using our PyGame GUI.
In this page, we will describe some of the features of our GUI.

The Board and Pieces
--------------------
Our GUI renders the Xiangqi environment's current game state upon calling
the environment object's :code:`render()` method.

During game mode, upon piece selection, the GUI will highlight the possible 
places on the board that the current selected piece can move to.

Captured Log
------------
The pieces that have been captured so far will be displayed in the captured log
section of the GUI

Sound Effects
-------------
Upon start up, the GUI will play a background music. In addition, there is an 
interesting 'knock' sound with every piece movement.
