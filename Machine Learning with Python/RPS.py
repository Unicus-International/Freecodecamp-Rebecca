# Import test functions:
from RPS_game import play, quincy, mrugesh, kris, abbey
# import random 
import random

# Initialize strategy tracking
my_last_move = ""
my_play_order = [{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }]
strategies = ['random', 'detect_pattern', 'counter_counter', 'exploit_mrugesh', 'counter_abbey']
strategy_flags = [True, True, True, True, True] # All strategies start as working
current_strategy = 0
my_history=[]
game_count = 0

# Main player function
def player(prev_play, opponent_history=[]):
    global my_last_move, current_strategy, strategy_flags, my_play_order, game_count

    # Reset history and strategy if 1000 games have been played
    if game_count % 1000 == 0:
        print("Resetting history and strategy after 1000 games.")
        opponent_history.clear()
        my_history.clear()
        my_play_order = [{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }]
        current_strategy = 0
        strategy_flags = [True, True, True, True, True]   # Reset all strategy flags to True

    # Increment game count
    game_count += 1

    if prev_play:
        opponent_history.append(prev_play)

    last_two = "".join(my_history[-2:])
    if len(last_two) == 2:
        my_play_order[0][last_two] += 1

    # Switch
    if strategies[current_strategy] == 'random':
        my_move = random.choice(["R", "P", "S"])
    elif strategies[current_strategy] == 'counter_counter':
        my_move = counter_move(counter_move(my_last_move))
    elif strategies[current_strategy] == 'detect_pattern':
        my_move = counter_move(detect_pattern(opponent_history))
    elif strategies[current_strategy] == 'exploit_mrugesh':
        my_move = counter_move(exploit_mrugesh(my_history))
    elif strategies[current_strategy] == 'counter_abbey':
        my_move = counter_move(predict_against_abbey(my_last_move, my_history, my_play_order))

    # Track the result
    if prev_play:
        if did_win(my_last_move, prev_play):
            # Strategy is working (win)
            strategy_flags[current_strategy] = True
        elif did_tie(my_last_move, prev_play):
            # Strategy can be considered working since you didn't lose
            strategy_flags[current_strategy] = True
        elif did_lose(my_last_move, prev_play):
            # Strategy is not working (loss)
            strategy_flags[current_strategy] = False
            switch_to_next_strategy()  # Switch to the next viable strategy

    print(strategies[current_strategy])
    my_last_move = my_move
    my_history.append(my_move)
    return my_move


# Cheat its abbey exept we copy her
def predict_against_abbey(prev_opponent_play,
          opponent_history=[],
          play_order=[]):

    if not prev_opponent_play:
        prev_opponent_play = 'R'
    opponent_history.append(prev_opponent_play)

    last_two = "".join(opponent_history[-2:])
    #if len(last_two) == 2:
        #play_order[0][last_two] += 1

    potential_plays = [
        prev_opponent_play + "R",
        prev_opponent_play + "P",
        prev_opponent_play + "S",
    ]

    sub_order = {
        k: play_order[0][k]
        for k in potential_plays if k in play_order[0]
    }

    prediction = max(sub_order, key=sub_order.get)[-1:]

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prediction]



# Function to switch to the next working strategy
def switch_to_next_strategy():
    global current_strategy, strategy_flags
    # Keep track of the original strategy to know if we've cycled through all
    original_strategy = current_strategy
    # Cycle through strategies until one has a True flag or start over
    for _ in range(len(strategies)):
        current_strategy = (current_strategy + 1) % len(strategies)
        if strategy_flags[current_strategy]:
            print(f"Switching strategy to: {strategies[current_strategy]}")
            return
    # If no working strategy is found, restart from the first strategy
    current_strategy = 0  # Start over
    strategy_flags = [True, True, True, True, True]



# Function to reset strategy flags (optional)
def reset_strategy_flags():
    global strategy_flags
    # Example: Reset all flags to True or implement your own logic
    strategy_flags = [True] * len(strategies)
    print("Resetting strategy flags.")

# Counter-counter strategy
def counter_move(move):
    return {"R": "P", "P": "S", "S": "R"}[move]

# Look for pattern in oponents move
def detect_pattern(opponent_history):
    if len(opponent_history) < 3:
        return random.choice(["R", "P", "S"])  # Not enough history yet

    # Search for the longest repeating pattern in the history
    for pattern_length in range(2, min(5, len(opponent_history))):
        recent_moves = opponent_history[-pattern_length:]
        for i in range(len(opponent_history) - pattern_length):
            if opponent_history[i:i + pattern_length] == recent_moves:
                # Pattern found, predict the next move
                if i + pattern_length < len(opponent_history):
                    return opponent_history[i + pattern_length]
    
    # No pattern found, return a random move
    return random.choice(["R", "P", "S"])


def did_win(my_move, opponent_move):
    win_cases = {"R": "S", "P": "R", "S": "P"}
    return win_cases[my_move] == opponent_move

def did_lose(my_move, opponent_move):
    loss_cases = {"R": "P", "P": "S", "S": "R"}
    return loss_cases[my_move] == opponent_move

def did_tie(my_move, opponent_move):
    return my_move == opponent_move

# New strategy to exploit mrugesh's predictability
def exploit_mrugesh(opponent_history):
    if not opponent_history:
        return random.choice(["R", "P", "S"])  # Random move if there's no history

    # Count the last moves
    last_ten = opponent_history[-10:]
    most_frequent = max(set(last_ten), key=last_ten.count)
    
    # Respond with the move that counters the counter move
    if most_frequent == 'R':
        return 'P'  # Play Paper against Rock
    elif most_frequent == 'P':
        return 'S'  # Play Scissors against Paper
    else:
        return 'R'  # Play Rock against Scissors
# test Playing the game
#play(player, quincy, 140, verbose=True) # OK
#play(player, kris, 300, verbose=True) # OK
#play(player, mrugesh, 200, verbose=True) # OK
play(player, abbey, 1001, verbose=True)



#Sample code:
"""
def player(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)

    guess = "R"
    if len(opponent_history) > 2:
        guess = opponent_history[-2]

    return guess
"""