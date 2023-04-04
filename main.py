import random
import termcolor
from TEALS_utils import get_valid_integer, safe_to_integer

MIN_NUMBER_OF_QUICKPICKS = 10  # Min number of quick picks we can buy
MAX_NUMBER_OF_QUICKPICKS = 50  # Max number of quick picks we can buy
NUMBER_OF_WHITEBALLS = 5  # Number of whiteballs to generate
NUMBER_OF_REDBALLS = 1  # Number of red balls (Powerball) to generate
HIGHEST_WHITEBALL = 69  # Highest value for white ball. In TX, they range from 1-69
HIGHEST_REDBALL = 26  # Highest value for red ball. In TX, they range from 1-26
COST_PER_TICKET = 2  # $2/quick pick ticket


# Name: get_seed_value
# Purpose: Prompt the user for a seed value for the randomization functions.
#          If none is provided, should use default (none) value
# Input: None
# Output: None
def get_seed_value():
    seed_value = input("Enter a seed value: ")
    if seed_value:
        random.seed(seed_value)
    else:
        random.seed()


# Name: get_number_of_quickpicks
# Purpose: Prompt the user for how many quick picks you want
#          to purchase. We can only purchase between 10-50 QPs
# Input: None
# Output: Number of quickpicks to purchase/generate
def get_number_of_quickpicks():
    """
    while True:
        prompt = str('How many quickpicks should we buy (%2d-%2d)? ' % (MIN_NUMBER_OF_QUICKPICKS, MAX_NUMBER_OF_QUICKPICKS))
        number = input(prompt)
        # Make sure we actually got a number and not some random string
        if number.isdigit():
            if MIN_NUMBER_OF_QUICKPICKS <= int(number) <= MAX_NUMBER_OF_QUICKPICKS:
                return int(number)
            else:
                print("'%2d' is outside of the allowed range. Please try again" % int(number))
        else:
         print("'%s' is not a number. Please try again" % number)
     """
    prompt = str('How many quickpicks should we buy (%2d-%2d)? ' % (MIN_NUMBER_OF_QUICKPICKS, MAX_NUMBER_OF_QUICKPICKS))
    return get_valid_integer(prompt, MIN_NUMBER_OF_QUICKPICKS, MAX_NUMBER_OF_QUICKPICKS)


# Name: generate_quick_pick
# Purpose: generate a single, quick pick Powerball lotto ticket
# Input: none
# Output: list containing the 5 whiteballs and 1 Powerball (redball)
#         Example: [1,22,42,51,60,22]
def generate_quick_pick():
    # Generate five unique numbers between 1 and 69
    white_balls = random.sample(range(1, HIGHEST_WHITEBALL + 1), NUMBER_OF_WHITEBALLS)

    # Sort the numbers in ascending order
    white_balls.sort()

    # Generate a single number between 1 and 26 for the red ball
    red_ball = random.sample(range(1, HIGHEST_REDBALL + 1), NUMBER_OF_REDBALLS)

    return white_balls + red_ball


# Name: display_quick_pick
# Purpose: Display a single quick pick properly
# Input: quick_pint_ticket (list) - Quick pick ticket to be displayed
# Output: ticket (str) containing the properly formatted QP string
def display_quick_pick(quick_pick_ticket):
    ticket = '%2d %2d %2d %2d %2d │ %s' % (quick_pick_ticket[0], quick_pick_ticket[1], quick_pick_ticket[2],
                                           quick_pick_ticket[3], quick_pick_ticket[4],
                                           termcolor.colored(quick_pick_ticket[5], 'red'))
    return ticket


# Name: get_winning_powerball_numbers
# Purpose: Prompt the user for this week's winning lottery numbers
#          1 - Prompt for white balls
#          2 - Prompt for red balls
#            Example: Please enter values for the white balls (1,2,3,4,5): 3,17,27,36,44
#                     Please enter Powerball number: 15
# Input: None
# Output: List containing the latest Powerball winning combination
#         Example: [3,17,27,36,44,15]
def get_winning_powerball_numbers():
    while True:
        whiteBalls = list(input("Please enter values for the white balls (1,2,3,4,5): ").split(','))
        # Forces us to get 5 and only 5 white balls
        if len(whiteBalls) == 5:
            break

    while True:
        redBalls = list(input("Please enter Powerball number: ").split(','))
        # There can be only one red ball (Powerball)
        if len(redBalls) == 1:
            break

    return list(map(safe_to_integer, whiteBalls + redBalls))


# Name: display_winning_ticket
# Purpose: Build a display string that shows matching numbers in green
# Input: quick_pick_ticket (list) - a single, quick pick ticket
#        winning_ticket (list) - winning Powerball ticket
# Output: str - formatted string showing the qp in the correct format
def display_winning_ticket(quick_pick_ticket, winning_ticket):
    ticket = ''

    # Did we match any of the other numbers
    for ball in range(0, NUMBER_OF_WHITEBALLS):
        if quick_pick_ticket[ball] in winning_ticket:
            ticket += '%s ' % termcolor.colored(str('%2d' % quick_pick_ticket[ball]), 'green')
        else:
            ticket += '%2d ' % quick_pick_ticket[ball]

    # Did we match the Powerball?
    if quick_pick_ticket[-1] == winning_ticket[-1]:
        ticket += '│ %s' % termcolor.colored(str('%2d' % quick_pick_ticket[-1]), 'green')
    else:
        ticket += '│ %2d' % quick_pick_ticket[-1]

    return ticket


# Name: calculate_winnings
# Purpose: Compare a quick pick ticket against the winning ticket and
# #        determine how much, if any, money we won
# Input: qp (list): a single quick pick ticket in this format [1,2,3,4,5,6]
#        winning_ticket (list): a list containing this week's winning Powerball numbers
# Output: total money won on this ticket (if any)
def calculate_winnings(quick_pick_ticket, winning_ticket):
    my_winnings = 0
    matching_white_balls = 0
    matched_powerball = False

    # Let's see if we matched the Powerball first
    if quick_pick_ticket[-1] == winning_ticket[-1]:
        matched_powerball = True
        my_winnings = 4

    # Did we match any of the other numbers
    for ball in range(0, NUMBER_OF_WHITEBALLS):
        if quick_pick_ticket[ball] in winning_ticket:
            matching_white_balls += 1

    '''
        • 5 Correct White Balls and the Powerball: Jackpot (starts at $40 million, has no upper limit)
        • 4 Correct White Balls and the Powerball: $50,000
        • 3 Correct White Balls and the Powerball: $100
        • 2 Correct White Balls and the Powerball: $7
        • 1 Correct White Ball and the Powerball: $4
        • No White Balls, Just the Powerball: $4
    '''
    if matched_powerball:
        if matching_white_balls == 1:
            my_winnings = 4
        if matching_white_balls == 2:
            my_winnings = 7
        if matching_white_balls == 3:
            my_winnings = 100
        if matching_white_balls == 4:
            my_winnings = 50000
        if matching_white_balls == 5:
            my_winnings = 40000000
    else:
        '''
            • 5 Correct White Balls, but no Powerball: $1,000,000
            • 4 Correct White Balls, but no Powerball: $100
            • 3 Correct White Balls, but no Powerball: $7
        '''
        if matching_white_balls == 3:
            my_winnings = 7
        if matching_white_balls == 4:
            my_winnings = 100
        if matching_white_balls == 5:
            my_winnings = 1000000

    return my_winnings


# Name: display_summary_winnings
# Purpose: Build a summary display of costs/winnings/overall net
# Input: total_winnings (float) - total of all lotto ticket winnings
#        total_ticket_cost (float) - how much did they spend on tickets?
# Output: str - formatted string showing the qp in the correct format
def display_summary_winnings(total_winnings, total_ticket_cost):
    print("┌─────────────────────────────────")
    print("│    Total winnings:  $%.2f" % total_winnings)
    print("│ Total ticket cost: ($%.2f)" % total_ticket_cost)
    print("│ ════════════════════════════════")

    # If we have a negative net, show it as ($nn.nn)
    if total_winnings - total_ticket_cost < 0:
        print("│      Net winnings: ($%.2f)" % abs(total_winnings - total_ticket_cost))
    else:
        print("│      Net winnings:  $%.2f" % (total_winnings - total_ticket_cost))

    print("└─────────────────────────────────")


# Main
# Let's initialize our random number generator.
get_seed_value()

# Lets setup some variables to use to track things
quickPicks = []
winningTicket = []
winningTickets = []
totalWinnings = 0
lifetimeWinnings = 0

# Let's print out all of our quick picks
numberOfQuickPicks = get_number_of_quickpicks()

# How much did all of these tickets cost?
totalTicketCost = numberOfQuickPicks * COST_PER_TICKET

print("\nHere are your Quick Picks")
# Generate however many quick picks were purchased
for i in range(numberOfQuickPicks):
    quickPick = generate_quick_pick()
    print("%2d: %s" % (i + 1, display_quick_pick(quickPick)))

    # Let's add this Quick Pick to our master list (quickPicks)
    quickPicks.append(quickPick)

# Let's get this week's winning Powerball combination
print("\n")
winningTicket = get_winning_powerball_numbers()

# Did we match anything?
for i in range(numberOfQuickPicks):
    winnings = calculate_winnings(quickPicks[i], winningTicket)
    if winnings == 0:
        print("{:2d}: {} Pays: {}".format(i + 1, display_winning_ticket(quickPicks[i], winningTicket),
                                          "${:,.2f}".format(winnings)))
    else:
        print("{:2d}: {} Pays: {}".format(i + 1, display_winning_ticket(quickPicks[i], winningTicket),
                                          termcolor.colored("${:,.2f}".format(winnings), 'green')))
    if winnings > 0:
        totalWinnings += winnings
        lifetimeWinnings += winnings
    # How much did we win/net?

display_summary_winnings(lifetimeWinnings, totalTicketCost)
