import pandas as pd
from tkinter import *


# help button, explaining the rules in a new window
def rules_help():
    rules_window = Toplevel(root, bg='white')
    label1 = Label(rules_window, text="Rules", font=('Times New Roman', 30, 'underline'), bg='white', pady=10)
    label2 = Label(rules_window, text="Welcome the the WORDLE game, created by Roy Ben-Zion. \n\n"
                                      "The rules of this game are simple: \n\n"
                                      "The computer has chosen a 5-letter English word, which you need to guess. \n"
                                      "You can type your guesses either by using your keyboard, or by pressing the "
                                      "buttons on screen with your mouse. \n"
                                      "After writing down your guess, press the Enter key, or the \"Enter Word\" "
                                      "button on screen, to receive feedback on your guess. \n"
                                      "(Your guess will only be accepted if it is a real English word, and is 5 "
                                      "letters long) \n"
                                      "After entering a guess, the computer will give you feedback, on the left side "
                                      "of the screen, on how close you were to the answer. \n\n"
                                      "* If a letter is marked with green, that means the letter correctly placed. \n"
                                      "* If a letter is marked with yellow, that means that the letter does exist, "
                                      "but in a different location. \n"
                                      "* If a letter is marked gray, that means that it does not appear in the "
                                      "answer. \n"
                                      "\n* If a letter appears more than once in your guess, then the amount of "
                                      "yellows\\greens will match the amount of times the letter appears in the "
                                      "answer. \n"
                                      "For example, if you guessed the word \"PUPPY\" and two of the P's are yellow, "
                                      "and one P is gray, it means that the answer has two P's only.\n"
                                      "\n"
                                      "You have 6 guesses to figure out the answer.\n"
                                      "Good Luck!")
    label2.config(font=('Arial', 15), justify='left', bg='white')
    label1.pack()
    label2.pack()


# showing your statistics
def stats():
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    # create bar chart
    ax = plt.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_label_coords(-.15, 0)
    plt.xlabel('Number of Guesses')
    plt.ylabel('Number\nof\nGames', rotation=0)
    plt.bar(df['score'], df['amount'])
    fig = plt.gcf()
    fig.subplots_adjust(left=0.2, bottom=0.1)

    # configuration for the case when there are no games in memory
    all_zeros = True
    for i in range(7):
        if df.iloc[i, 1] != 0:
            all_zeros = False
            break
    if all_zeros:
        plt.ylim([0, 1.05])

    # title, labels and buttons
    new_window = Toplevel(root, bg='white')
    label1 = Label(new_window, text="Your Statistics", font=('Times New Roman', 30, 'underline'), bg='white',
                   pady=10).pack()

    canvas = FigureCanvasTkAgg(fig, new_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(padx=50)

    frame_button = Frame(new_window, pady=25, bg='white')
    frame_button.pack()

    reset_button = Button(frame_button, text='RESET SCORES', font=('Arial', 10, 'bold'),
                          command=lambda: reset_sure(new_window), cursor="hand2",
                          pady=10, relief='solid', borderwidth=1, bg='red')

    go_back_button = Button(frame_button, text='Go Back', font=('Arial', 10), command=new_window.destroy,
                            cursor="hand2",
                            pady=10, relief='solid', borderwidth=1)

    reset_button.grid(row=0, column=0, padx=10)
    go_back_button.grid(row=0, column=1, padx=17)


# reset personal scores
def reset_scores(window):
    for row in range(7):
        df.iloc[row, 1] = 0
    df.to_csv('scores.csv', index=False)
    stats()
    window.destroy()


# check the word we typed is valid,and enters it if it is
def enter():
    global current_row
    global letter_index
    global typed_word

    # a word can't be entered if it doesn't have 5 letters
    if letter_index != 5:
        return
    else:
        # check if the word is in the valid-words list, and if it is, use the 'check_word' function, to find how
        # close it is to the solution
        if typed_word in wordlist:
            check_word(typed_word)

            # prepare for a new letter to be typed, after we entered the last one
            typed_word = ''
            letter_index = 0
            current_row += 1


# add a letter onto the screen, and to our variable 'typed_word'
def virtual_type(letter):
    global letter_index
    global current_row
    global typed_word

    # if we already entered 5 letters, no more letters can be added
    if letter_index < 5:
        t[current_row][letter_index].config(text=letter.upper())
        letter_index += 1
        typed_word += letter


# delete a letter from screen, and from our 'typed_word' variable
def virtual_delete():
    global letter_index
    global current_row
    global typed_word

    # the if statement makes sure we don't delete more letters than we have
    if letter_index > 0:
        t[current_row][letter_index - 1].config(text='')
        letter_index -= 1
        typed_word = typed_word[:-1]


# check our entered word for greens and yellows
def check_word(word):
    global current_row

    # create a list with all the letters that are in the answer, to help us find yellows. we will edit the list while
    # we check for the answer, so we don't count the same letter more than once as a yellow
    possible_yellows = list(answer)

    # a list of all indexes that aren't green. if the list is empty, we know we won
    non_green_indexes = []

    # check for greens
    for i in range(5):
        if word[i] == answer[i]:

            #change color to green, both on the left side, and the right side of the screen
            t[current_row][i].config(bg="green")
            letters[word[i].upper()].config(bg="green")

            # a single letter can't be both green and yellow, so it must be removed
            # from the list we draw yellows from
            possible_yellows.remove(word[i])

        else:
            non_green_indexes.append(i)

    # if all the letters are green, we won
    if len(non_green_indexes) == 0:
        win()

    # if we didn't win, and we used up all our available guesses, we lost
    elif current_row == 5:
        lose()

    # checking for yellows, withing the indexes that aren't green
    for i in non_green_indexes:
        if word[i] in possible_yellows:
            t[current_row][i].config(bg="yellow")
            possible_yellows.remove(word[i])

            #change the keyboard color to yellow, only if it isn't already green
            if letters[word[i].upper()]["background"] != "green":
                letters[word[i].upper()].config(bg="yellow")
        else:
            t[current_row][i].config(bg="gray")

            # change the keyboard color to gray, only if it isn't already green or yellow
            if letters[word[i].upper()]["background"] not in ["green", "yellow"]:
                letters[word[i].upper()].config(bg="gray")


# start a new game
def start_over(window):
    global answer
    global current_row
    global letter_index
    global typed_word
    global new_window

    # pick a new solution
    answer = answers.sample().iloc[0][0]

    #reset all colors
    for i in range(6):
        for j in range(5):
            t[i][j].config(bg=root['background'], text="")
    for i in letters.values():
        i.config(bg=root['background'], state=NORMAL)

    # make all keys usable again
    bind_all_keys()

    # return to the first row
    current_row = 0

    # close the window that asked us to play again
    window.destroy()


# winning sequence
def win():

    # make all keys unusable
    unbind_all_keys()

    # write to log
    df.iloc[current_row, 1] += 1
    df.to_csv('scores.csv', index=False)

    # open a winning window
    new_window = Toplevel(root, bg='white')
    new_window.geometry('400x200')
    label1 = Label(new_window, text="You Won!", font=('Arial', 30, 'underline'), fg='green', bg='white', pady=10).pack()

    # if we won with our first guess, have a fitting label
    if current_row == 0:
        label2 = Label(new_window, text="You guessed the word \"" + answer + "\" in 1 guess", bg='white',
                       font=('Arial', 15)).pack()
    # if we took more than one guess, write the number of guesses we used
    else:
        label2 = Label(new_window,
                       text="you guessed the word \"" + answer + "\" in " + str(current_row + 1) + " guesses",
                       bg='white', font=('Arial', 15)).pack()


    # buttons for starting again or showing statistics
    frame_buttons = Frame(new_window, pady=15, bg='white')

    again_button = Button(frame_buttons, text='Play Again', font=('Arial', 10), command=lambda: start_over(new_window),
                          cursor="hand2",
                          relief='solid', borderwidth=1)
    stats_button = Button(frame_buttons, text='Personal Stats', font=('Arial', 10), command=stats, cursor="hand2",
                          justify='right', relief='solid', borderwidth=1)
    frame_buttons.pack()
    again_button.grid(row=0, column=0, padx=10)
    stats_button.grid(row=0, column=1, padx=17)


# losing sequence
def lose():

    # make all keys unusable
    unbind_all_keys()

    # write to log
    df.iloc[6, 1] += 1
    df.to_csv('scores.csv', index=False)

    # open a losing window
    new_window = Toplevel(root, bg='white')
    new_window.geometry('400x200')
    label1 = Label(new_window, text="You Lost", font=('Arial', 30, 'underline'), fg='red', bg='white', pady=10).pack()
    word_was = Label(new_window, text="The word was: " + answer, bg='white', font=('Arial', 15)).pack()
    label2 = Label(new_window, text="Better luck next time!", bg='white', font=('Arial', 15), pady=15).pack()

    # buttons for starting again or showing statistics
    frame_buttons = Frame(new_window, pady=15, bg='white')

    again_button = Button(frame_buttons, text='Play Again', font=('Arial', 10), command=lambda: start_over(new_window),
                          cursor="hand2",
                          relief='solid', borderwidth=1)
    stats_button = Button(frame_buttons, text='Personal Stats', font=('Arial', 10), command=stats, cursor="hand2",
                          justify='right', relief='solid', borderwidth=1)
    frame_buttons.pack()
    again_button.grid(row=0, column=0, padx=10)
    stats_button.grid(row=0, column=1, padx=17)


# activate all keys, both virtual and on keyboard
def bind_all_keys():

    # activate the buttons on screen
    Enter_button.config(state=NORMAL, cursor='hand2')
    give_up_button.config(state=NORMAL, cursor='hand2')
    BACK.config(state=NORMAL, cursor='hand2')
    for i in letters.values():
        i.config(state=NORMAL, cursor='hand2')

    # activate all keyboard keys
    root.bind('a', lambda i: virtual_type('a'))
    root.bind('b', lambda i: virtual_type('b'))
    root.bind('c', lambda i: virtual_type('c'))
    root.bind('d', lambda i: virtual_type('d'))
    root.bind('e', lambda i: virtual_type('e'))
    root.bind('f', lambda i: virtual_type('f'))
    root.bind('g', lambda i: virtual_type('g'))
    root.bind('h', lambda i: virtual_type('h'))
    root.bind('i', lambda i: virtual_type('i'))
    root.bind('j', lambda i: virtual_type('j'))
    root.bind('k', lambda i: virtual_type('k'))
    root.bind('l', lambda i: virtual_type('l'))
    root.bind('m', lambda i: virtual_type('m'))
    root.bind('n', lambda i: virtual_type('n'))
    root.bind('o', lambda i: virtual_type('o'))
    root.bind('p', lambda i: virtual_type('p'))
    root.bind('q', lambda i: virtual_type('q'))
    root.bind('r', lambda i: virtual_type('r'))
    root.bind('s', lambda i: virtual_type('s'))
    root.bind('t', lambda i: virtual_type('t'))
    root.bind('u', lambda i: virtual_type('u'))
    root.bind('v', lambda i: virtual_type('v'))
    root.bind('w', lambda i: virtual_type('w'))
    root.bind('x', lambda i: virtual_type('x'))
    root.bind('y', lambda i: virtual_type('y'))
    root.bind('z', lambda i: virtual_type('z'))

    root.bind('A', lambda i: virtual_type('a'))
    root.bind('B', lambda i: virtual_type('b'))
    root.bind('C', lambda i: virtual_type('c'))
    root.bind('D', lambda i: virtual_type('d'))
    root.bind('E', lambda i: virtual_type('e'))
    root.bind('F', lambda i: virtual_type('f'))
    root.bind('G', lambda i: virtual_type('g'))
    root.bind('H', lambda i: virtual_type('h'))
    root.bind('I', lambda i: virtual_type('i'))
    root.bind('J', lambda i: virtual_type('j'))
    root.bind('K', lambda i: virtual_type('k'))
    root.bind('L', lambda i: virtual_type('l'))
    root.bind('M', lambda i: virtual_type('m'))
    root.bind('N', lambda i: virtual_type('n'))
    root.bind('O', lambda i: virtual_type('o'))
    root.bind('P', lambda i: virtual_type('p'))
    root.bind('Q', lambda i: virtual_type('q'))
    root.bind('R', lambda i: virtual_type('r'))
    root.bind('S', lambda i: virtual_type('s'))
    root.bind('T', lambda i: virtual_type('t'))
    root.bind('U', lambda i: virtual_type('u'))
    root.bind('V', lambda i: virtual_type('v'))
    root.bind('W', lambda i: virtual_type('w'))
    root.bind('X', lambda i: virtual_type('x'))
    root.bind('Y', lambda i: virtual_type('y'))
    root.bind('Z', lambda i: virtual_type('z'))

    root.bind('<BackSpace>', lambda i: virtual_delete())
    root.bind('<Return>', lambda i: enter())


# deactivate all keys. function is used once a player wins/loses
def unbind_all_keys():

    # deactivate the buttons on screen
    Enter_button.config(state=DISABLED, cursor='arrow')
    give_up_button.config(state=DISABLED, cursor='arrow')
    BACK.config(state=DISABLED, cursor='arrow')
    for i in letters.values():
        i.config(state=DISABLED, cursor='arrow')

    # deactivate all keyboard buttons
    for i in letters.keys():
        root.unbind(i)
        root.unbind(i.lower())

    root.unbind('<BackSpace>')
    root.unbind('<Return>')


# asks if you're sure that you want to reset scores
def reset_sure(window):
    new_window = Toplevel(root)

    frame_buttons = Frame(new_window, pady=15)

    label1 = Label(new_window, text="Are You Sure?", font=('Arial', 30, 'bold'), pady=10).pack()

    # button for playing again
    again_button = Button(frame_buttons, text='Yes, resest', font=('Arial', 10),
                          command=lambda: [reset_scores(window), new_window.destroy()],
                          cursor="hand2",
                          relief='solid', borderwidth=1)

    #button for showing statistics
    stats_button = Button(frame_buttons, text='No', font=('Arial', 10), command=new_window.destroy, cursor="hand2",
                          justify='right', relief='solid', borderwidth=1)
    frame_buttons.pack()
    again_button.grid(row=0, column=0, padx=10)
    stats_button.grid(row=0, column=1, padx=17)


root = Tk()

# words that are common enough to be picked by the computer
answers = pd.read_csv("answers.txt", header=None)

# all 5-letter words, other than the previous list, that are considered valid in English, and can be guessed
allowed = pd.read_csv("allowed.txt", header=None)

# randomly pick a solution
answer = answers.sample().iloc[0][0]

# combine all possible guesses into a single list
wordlist = set(answers.iloc[:, 0]) | set(allowed.iloc[:, 0])

# read the scoreboard, so we can adjust it after winning/losing
df = pd.read_csv('scores.csv')

frame_left = Frame(root, padx=10, pady=15)
frame_left.grid(row=0, column=0)

frame_right = Frame(root, padx=10, pady=0)
frame_right.grid(row=0, column=1)

game_title_frame = Frame(frame_right, pady=20)
keyboard_frame = Frame(frame_right)
frame_right2 = Frame(frame_right, pady=10)

game_title_frame.pack()
keyboard_frame.pack()
frame_right2.pack()

# keyboard frames
keyboard_up = Frame(keyboard_frame)
keyboard_middle = Frame(keyboard_frame)
keyboard_bottom = Frame(keyboard_frame)

keyboard_up.grid(row=0, column=0)
keyboard_middle.grid(row=1, column=0)
keyboard_bottom.grid(row=2, column=0)

Enter_button = Button(frame_right2, text='Enter Word', font=('Arial', 10), command=lambda: enter(), cursor="hand2",
                      pady=10, relief='solid', borderwidth=1)
give_up_button = Button(frame_right2, text='Give Up', font=('Arial', 10, 'bold'), command=lambda: lose(),
                        cursor="hand2", pady=10, justify='right', relief='solid', borderwidth=1, bg='#FF3632',
                        fg='white')

Enter_button.grid(row=0, column=0, padx=10)
give_up_button.grid(row=0, column=1, padx=17)

wordle_title = Label(game_title_frame, text='WORDLE', font=('Times New Roman', 40, 'underline'), anchor='n').pack()
credits = Label(game_title_frame, text="Home-Made Edition by Roy Ben-Zion", font=('Cambria', 20)).pack()
rules_and_stats = Frame(game_title_frame, pady=10)
rules_and_stats_left = Frame(rules_and_stats, padx=25)
rules_and_stats_right = Frame(rules_and_stats, padx=25)
rules = Button(rules_and_stats_left, text="Rules", command=rules_help, cursor="question_arrow", width=6, height=2,
               relief='solid', borderwidth=1, pady=2, padx=10)
stats_frame = Button(rules_and_stats_right, text="Personal Stats", command=stats, cursor="hand2", width=6, height=2,
                     relief='solid', borderwidth=1, pady=2, padx=17)

rules_and_stats.pack()
rules_and_stats_left.grid(row=0, column=0)
rules_and_stats_right.grid(row=0, column=1)
rules.pack()
stats_frame.pack()

# create a board we can add our guesses to
t = []
for i in range(6):
    t.append([])
    for j in range(5):
        t[i].append("t" + str(i) + str(j))
        t[i][j] = Label(frame_left, width=4, height=2, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'))
        t[i][j].grid(row=i, column=j, sticky="nsew")

# create a virtual keyboard

Q = Button(keyboard_up, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'), text='Q',
           cursor="hand2", command=lambda: virtual_type('q'))
W = Button(keyboard_up, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'), text='W',
           cursor="hand2", command=lambda: virtual_type('w'))
E = Button(keyboard_up, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'), text='E',
           cursor="hand2", command=lambda: virtual_type('e'))
R = Button(keyboard_up, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'), text='R',
           cursor="hand2", command=lambda: virtual_type('r'))
T = Button(keyboard_up, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'), text='T',
           cursor="hand2", command=lambda: virtual_type('t'))
Y = Button(keyboard_up, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'), text='Y',
           cursor="hand2", command=lambda: virtual_type('y'))
U = Button(keyboard_up, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'), text='U',
           cursor="hand2", command=lambda: virtual_type('u'))
I = Button(keyboard_up, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'), text='I',
           cursor="hand2", command=lambda: virtual_type('i'))
O = Button(keyboard_up, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'), text='O',
           cursor="hand2", command=lambda: virtual_type('o'))
P = Button(keyboard_up, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'), text='P',
           cursor="hand2", command=lambda: virtual_type('p'))

A = Button(keyboard_middle, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='A', cursor="hand2", command=lambda: virtual_type('a'))
S = Button(keyboard_middle, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='S', cursor="hand2", command=lambda: virtual_type('s'))
D = Button(keyboard_middle, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='D', cursor="hand2", command=lambda: virtual_type('d'))
F = Button(keyboard_middle, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='F', cursor="hand2", command=lambda: virtual_type('f'))
G = Button(keyboard_middle, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='G', cursor="hand2", command=lambda: virtual_type('g'))
H = Button(keyboard_middle, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='H', cursor="hand2", command=lambda: virtual_type('h'))
J = Button(keyboard_middle, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='J', cursor="hand2", command=lambda: virtual_type('j'))
K = Button(keyboard_middle, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='K', cursor="hand2", command=lambda: virtual_type('k'))
L = Button(keyboard_middle, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='L', cursor="hand2", command=lambda: virtual_type('l'))

Z = Button(keyboard_bottom, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='Z', cursor="hand2", command=lambda: virtual_type('z'))
X = Button(keyboard_bottom, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='X', cursor="hand2", command=lambda: virtual_type('x'))
C = Button(keyboard_bottom, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='C', cursor="hand2", command=lambda: virtual_type('c'))
V = Button(keyboard_bottom, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='V', cursor="hand2", command=lambda: virtual_type('v'))
B = Button(keyboard_bottom, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='B', cursor="hand2", command=lambda: virtual_type('b'))
N = Button(keyboard_bottom, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='N', cursor="hand2", command=lambda: virtual_type('n'))
M = Button(keyboard_bottom, width=2, height=1, borderwidth=1, padx=0, relief=SOLID, font=('Arial', 25, 'bold'),
           text='M', cursor="hand2", command=lambda: virtual_type('m'))
BACK = Button(keyboard_bottom, width=2, height=1, borderwidth=1, padx=6, pady=7, relief=SOLID,
              font=('Arial', 20, 'bold'), text='←', cursor="hand2", command=lambda: virtual_delete())

Q.grid(row=0, column=0)
W.grid(row=0, column=1)
E.grid(row=0, column=2)
R.grid(row=0, column=3)
T.grid(row=0, column=4)
Y.grid(row=0, column=5)
U.grid(row=0, column=6)
I.grid(row=0, column=7)
O.grid(row=0, column=8)
P.grid(row=0, column=9)

A.grid(row=0, column=0)
S.grid(row=0, column=1)
D.grid(row=0, column=2)
F.grid(row=0, column=3)
G.grid(row=0, column=4)
H.grid(row=0, column=5)
J.grid(row=0, column=6)
K.grid(row=0, column=7)
L.grid(row=0, column=8)

Z.grid(row=0, column=0)
X.grid(row=0, column=1)
C.grid(row=0, column=2)
V.grid(row=0, column=3)
B.grid(row=0, column=4)
N.grid(row=0, column=5)
M.grid(row=0, column=6)
BACK.grid(row=0, column=7)

# a dictionary connection a letter to its virtual key on screen
letters = {"Q": Q, "W": W, "E": E, "R": R, 'T': T, 'Y': Y, 'U': U, "I": I, "O": O, "P": P, "A": A, "S": S, "D": D,
           "F": F, "G": G, "H": H, "J": J, "K": K, "L": L, "Z": Z, "X": X, "C": C, "V": V, "B": B, "N": N, "M": M}

# the row we currently type in starts at 0
current_row = 0

# the column we add a letter to starts at 0
letter_index = 0

# the new word we typed
typed_word = ''

# activate all keys
bind_all_keys()

# start the program
root.mainloop()
