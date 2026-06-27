""" Slot Machine - see README for details."""

import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A" : 2,
    "B" : 4,
    "C" : 6,
    "D" : 8
}

symbol_value = {
    "A" : 5,
    "B" : 4,
    "C" : 3,
    "D" : 2
}


def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    
    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        
        columns.append(column)

    return columns


def print_slot_machine(columns): #Displays the slot machine grid in the terminal
    for row in range(len(columns [0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end = "")
        print()

def deposit():

    while True: #The amount deposited has to be valid
        amount = input("Select the amount you want to deposit : €")
        if amount.isdigit(): #The amount must be a positive number
            amount = int(amount)
            if amount > 0:  #The amount deposited has to be positive
                break
            else:
                print("The amount has to be positive")
        else:
            print("The amount must be a number")

    return amount

def get_number_of_lines(): #The player chooses how many lines to bet on
    while True: #The number of lines has to be valid
        lines = input(f"Select the number of lines you want to bet on (1 - {MAX_LINES}): ")
        if lines.isdigit(): #The number of lines must be a number
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:  #The number of lines has to be within the valid range
                break
            else:
                print(f"The number of lines has to be between 1 and {MAX_LINES}")
        else:
            print("The number of lines must be a number")
    return lines

def get_bet(): #The player chooses the amount he wants to bet on
    while True: #The bet has to be valid
        bet = input(f"What would you like to bet on each line? ({MIN_BET} - {MAX_BET}): ")
        if bet.isdigit(): #The bet must be a number
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:  #The bet has to be within the valid range
                break
            else:
                print(f"The bet has to be between {MIN_BET} and {MAX_BET}")
        else:
            print("The bet must be a number")
    return bet



def spin(balance):
    lines = get_number_of_lines()
    while True: #Keep asking until the bet is within the user's balance
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"Your current balance is {balance}€, you don't have enough money to bet {total_bet}")
        else:
            break


    print(f"You are betting {bet}€ on {lines} lines. Total bet is equal to: {total_bet}€")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won €{winnings}")
    print(f"You won on lines:", *winning_lines)
    return winnings - total_bet


def main(): #The function that runs the entire game
    balance = deposit()
    while True:
        print(f"Current balance is €{balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)

    print(f"You left with €{balance}")

main()


