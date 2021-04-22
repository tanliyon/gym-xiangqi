import numpy as np
import random
import tensorflow as tf
import copy

from collections import defaultdict
from gym_xiangqi.utils import action_space_to_move
from gym_xiangqi.constants import ALLY, TOTAL_POS, PIECE_CNT

BATCH_SIZE = 4
INVALID_MOVE_Q = -999999999

class QLearningAgent:
    """
    This is the implementation of Deep Q-learning
    Network (DQN) for XiangQi using Keras.
    """
    def __init__(self, load_path, discount_rate=0.8, epsilon=0.2, buffer_length=1000):
        if load_path:
            print(f"Loading model from {load_path}...")
            # Load model
            self.model = tf.keras.models.load_model(load_path)
            print("Model loaded!")
        else:
            self.model = self.make_model()
        self.model_target = self.make_model()
        self.discount_rate = discount_rate
        self.epsilon = epsilon
        self.buffer_length = buffer_length
        # Replay buffer entries are [state, action, reward, next_state].
        self.replay_buffer = []
    
    def make_model(self):
        inputs = tf.keras.Input(shape=(90,))
        dense_1 = tf.keras.layers.Dense(128, activation=tf.nn.relu)(inputs)
        dense_2 = tf.keras.layers.Dense(256, activation=tf.nn.relu)(dense_1)
        dense_3 = tf.keras.layers.Dense(256, activation=tf.nn.relu)(dense_2)
        outputs = tf.keras.layers.Dense(TOTAL_POS * TOTAL_POS * PIECE_CNT, activation=tf.nn.softmax)(dense_3)
        return tf.keras.Model(inputs=inputs, outputs=outputs)
    
    def update(self, state, next_state, action, reward, loss_fn, optimizer):
        """
        Main function that updates the network based on the action taken
        and reward received.
        """
        if len(self.replace_buffer) > self.buffer_length:
            self.replace_buffer.pop(0)
        self.replay_buffer.append([state, action, reward, next_state])
        states, actions, rewards, next_states = self.sample_replay_buffer()
        future_actions_rewards = self.model_target.predict(self.process_input(next_states))
        expected_q_values = rewards + self.discount_rate*tf.reduce_max(future_actions_rewards, axis=1)
        mask = tf.one_hot(actions, TOTAL_POS * TOTAL_POS * PIECE_CNT)
        with tf.GradientTape() as tape:
            q_values = self.model(self.process_input(states))
            relevant_q_values = tf.reduce_sum(tf.multiply(mask, q_values), axis=1)
            loss = loss_fn(expected_q_values, relevant_q_values)
        
        grads = tape.gradient(loss, self.model.trainable_variables)
        optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
        return loss

    def sample_replay_buffer(self):
        """
        Sample BATCH_SIZE amount of samples randomly
        from the replay buffer.
        """
        states = np.zeros((BATCH_SIZE, 10, 9))
        actions = np.zeros(BATCH_SIZE)
        rewards = np.zeros(BATCH_SIZE)
        next_states = np.zeros((BATCH_SIZE, 10, 9))
        for i in range(BATCH_SIZE):
            state, action, reward, next_state = random.choice(self.replay_buffer)
            states[i] = state
            actions[i] = action
            rewards[i] = reward
            next_states[i] = next_state
        return states, actions, rewards, next_states
    
    def update_target_network(self):
        """
        Copy over the weghts from the model to the target model.
        This should be done periodically to have a more stable target.
        """
        self.model_target.set_weights(self.model.get_weights())
            
    def save(self, path):
        """
        Save model to path.
        """
        print(f"Saving model to {path}...")
        self.model.save(path)
        print(f"Model saved!")

    def process_input(self, state):
        """
        Given a state, reshape and process it before feeding
        it into the network.
        """
        if len(state.shape) < 3:
            state = tf.expand_dims(state, axis=0)
        state = np.reshape(state, (-1, 90))
        return state

    def exploit(self):
        """
        Simple fixed-value epsilon-greedy policy.
        """
        if random.uniform(0, 1) > self.epsilon:
            return True
        return False

    def move(self, env):
        """
        Make a move based on the environment.
        """
        actions = (env.ally_actions if env.turn == ALLY
            else env.enemy_actions)
        legal_moves = np.where(actions == 1)[0]
        
        # Exploit.
        if self.exploit():
            # We want to mask the invalid actions, so flip 
            # invalid actions = 1, valid actions = 0.
            mask = copy.deepcopy(actions)
            mask[actions == 1] = 0
            mask[actions == 0] = 1
            mask_legal_moves = self.model(self.process_input(env._state)) + (mask * INVALID_MOVE_Q)
            action = tf.argmax((mask_legal_moves), axis=1).numpy()[0]
            assert action in legal_moves
            assert actions[action] == 1
            return action

        # Explore
        ind = random.randint(0, len(legal_moves)-1)
        return legal_moves[ind]
