# Rockpaperscissorsproject
import wx
import random
from CSVFORSTORE import *


# --- Transparent Text Class ---
class TransparentText(wx.StaticText):
    def __init__(self, parent, id=wx.ID_ANY, label='',
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.TRANSPARENT_WINDOW, name='transparenttext'):
        super().__init__(parent, id, label, pos, size, style, name)

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_paint(self, event):
        bdc = wx.PaintDC(self)
        dc = wx.GCDC(bdc)

        font_face = self.GetFont()
        font_color = self.GetForegroundColour()

        dc.SetFont(font_face)
        dc.SetTextForeground(font_color)
        dc.DrawText(self.GetLabel(), 0, 0)

    def on_size(self, event):
        self.Refresh()
        event.Skip()


# --- GAME VARIABLES ---
player1 = "User"
player2 = "Bot"
is_two_player = False
player1_choice = None
player2_choice = None
waiting_for_player2 = False

s = 0
x = 0
ranusch = 0
botchoicein = 0
round_count = 0
max_rounds = 5
result_texts = []


def botgame():
    global player1, player2, is_two_player
    player1 = "User"
    player2 = "Bot"
    is_two_player = False
    restart_game(None)

    pvp.Hide()
    bot_btn.Hide()
    stone.Show()
    paper.Show()
    scissors.Show()
    Rand.Show()

    stone.Enable(True)
    paper.Enable(True)
    scissors.Enable(True)
    Rand.Enable(True)
    clear_result_texts()


def twoplayergame():
    global player1, player2, is_two_player
    player1 = "Player 1"
    player2 = "Player 2"
    is_two_player = True
    restart_game(None)
    # Hide mode selection buttons
    pvp.Hide()
    bot_btn.Hide()
    # Show and enable game buttons
    stone.Show()
    paper.Show()
    scissors.Show()
    Rand.Show()
    stone.Enable(True)
    paper.Enable(True)
    scissors.Enable(True)
    Rand.Enable(True)
    clear_result_texts()


def botchoice():
    global botchoicein
    botchoicein = random.randint(0, 2)


def randomuserchoice(event):
    global ranusch
    ranusch = random.randint(0, 2)
    choice = ["Rock", "Paper", "Scissors"]
    play_round(choice[ranusch])


def clear_result_texts():
    global result_texts
    for text in result_texts:
        text.Destroy()
    result_texts = []


def show_game_over():
    clear_result_texts()

    large_font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    medium_font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

    game_over_text = TransparentText(panel, label="GAME OVER!", pos=(550, 300))
    game_over_text.SetFont(large_font)
    game_over_text.SetForegroundColour(wx.Colour(255, 0, 0))
    result_texts.append(game_over_text)

    if s > x:
        winner_text = TransparentText(panel, label=f"{player1} WINS!  Final Score - {player1}: {s}, {player2}: {x}",pos=(400, 350))
        winner_text.SetForegroundColour(wx.Colour(1, 135, 255))
    elif x > s:
        winner_text = TransparentText(panel, label=f"{player2} WINS! Final Score - {player1}: {s}, {player2}: {x}",pos=(400, 350))
        winner_text.SetForegroundColour(wx.RED)
    else:
        winner_text = TransparentText(panel, label=f"IT'S A TIE! Final Score - {player1}: {s}, {player2}: {x}",pos=(400, 350))
        winner_text.SetForegroundColour(wx.Colour(171, 1, 255))

    winner_text.SetFont(medium_font)
    result_texts.append(winner_text)

    restart_btn = wx.Button(panel, label="Restart Game", size=(120, 40), pos=(520, 400))
    restart_btn.Bind(wx.EVT_BUTTON, restart_game)
    result_texts.append(restart_btn)

    # Add back to menu button
    menu_btn = wx.Button(panel, label="Back to Menu", size=(120, 40), pos=(650, 400))
    menu_btn.Bind(wx.EVT_BUTTON, back_to_menu)
    result_texts.append(menu_btn)
    write_game_result(s,x,player1,player2)

    stone.Enable(False)
    paper.Enable(False)
    scissors.Enable(False)
    Rand.Enable(False)


def back_to_menu(event):
    """Return to the main menu"""
    global s, x, round_count, player1_choice, player2_choice, waiting_for_player2
    s = 0
    x = 0
    round_count = 0
    player1_choice = None
    player2_choice = None
    waiting_for_player2 = False
    clear_result_texts()

    # Hide game buttons
    stone.Hide()
    paper.Hide()
    scissors.Hide()
    Rand.Hide()

    mode_text = TransparentText(panel, label="Choose Game Mode", pos=(520, 230))
    medium_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    mode_text.SetFont(medium_font)
    mode_text.SetForegroundColour(wx.Colour(7, 148, 158))
    result_texts.append(mode_text)

    # Show mode selection buttons
    pvp.Show()
    bot_btn.Show()


def restart_game(event):
    global s, x, round_count, player1_choice, player2_choice, waiting_for_player2
    s = 0
    x = 0
    round_count = 0
    player1_choice = None
    player2_choice = None
    waiting_for_player2 = False
    clear_result_texts()
    stone.Enable(True)
    paper.Enable(True)
    scissors.Enable(True)
    Rand.Enable(True)


def stonein(event):
    play_round("Rock")


def paperin(event):
    play_round("Paper")


def scissorsin(event):
    play_round("Scissors")


def play_round(user_choice):
    global s, x, round_count, player1_choice, player2_choice, waiting_for_player2

    if round_count >= max_rounds:
        return

    # Two-player mode logic
    if is_two_player:
        if not waiting_for_player2:
            # Player 1's turn
            player1_choice = user_choice
            waiting_for_player2 = True
            clear_result_texts()

            small_font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            waiting_text = TransparentText(panel, label=f"{player1} chose! Now {player2}'s turn...", pos=(480, 300))
            waiting_text.SetFont(small_font)
            waiting_text.SetForegroundColour(wx.Colour(171, 1, 255))
            result_texts.append(waiting_text)
            return
        else:
            # Player 2's turn
            player2_choice = user_choice
            waiting_for_player2 = False
            round_count += 1

            # Now process the round with both choices
            process_round(player1_choice, player2_choice)
    else:
        # Bot mode (original logic)
        round_count += 1
        botchoice()
        choices = ["Rock", "Paper", "Scissors"]
        bot_choice = choices[botchoicein]
        process_round(user_choice, bot_choice)


def process_round(choice1, choice2):
    global s, x

    clear_result_texts()

    small_font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

    round_text = TransparentText(panel, label=f"Round {round_count}/{max_rounds}", pos=(580, 150))
    round_text.SetFont(small_font)
    result_texts.append(round_text)
    round_text.SetForegroundColour(wx.Colour(7, 148, 158))

    text2 = TransparentText(panel, label=f"{player1}'s choice: {choice1}", pos=(450, 300))
    text3 = TransparentText(panel, label=f"{player2}'s choice: {choice2}", pos=(650, 300))
    text2.SetForegroundColour(wx.Colour(1, 135, 255))
    text3.SetForegroundColour(wx.RED)
    text2.SetFont(small_font)
    text3.SetFont(small_font)
    result_texts.extend([text2, text3])

    if choice1 == choice2:
        n = "tie"
        tie1 = TransparentText(panel, label="Match was a Tie!", pos=(550, 330))
        tie2 = TransparentText(panel, label=f"{player1} score: {s}", pos=(450, 360))
        tie3 = TransparentText(panel, label=f"{player2} score: {x}", pos=(650, 360))
        tie2.SetFont(small_font)
        tie3.SetFont(small_font)
        tie2.SetForegroundColour(wx.Colour(1, 135, 255))
        tie3.SetForegroundColour(wx.RED)
        tie1.SetFont(small_font)
        result_texts.extend([tie1, tie2, tie3])
        tie1.SetForegroundColour(wx.Colour(171, 1, 255))

    elif (choice1 == "Rock" and choice2 == "Scissors") or \
            (choice1 == "Paper" and choice2 == "Rock") or \
            (choice1 == "Scissors" and choice2 == "Paper"):
        n = "win"
        s += 1
        win1 = TransparentText(panel, label=f"{player1} won! Score: {s}", pos=(425, 330))
        win2 = TransparentText(panel, label=f"{player2} score: {x}", pos=(650, 330))

        if not is_two_player:
            win3 = TransparentText(panel, label=f"Bot: You were Lucky this time but not forever!!", pos=(450, 360))
            win3.SetForegroundColour(wx.RED)
            win3.SetFont(small_font)
            result_texts.append(win3)

        win1.SetForegroundColour(wx.Colour(1, 135, 255))
        win2.SetForegroundColour(wx.RED)
        win1.SetFont(small_font)
        win2.SetFont(small_font)
        result_texts.extend([win1, win2])

    else:
        n = "lose"
        x += 1
        lost1 = TransparentText(panel, label=f"{player1} lost! Score: {s}", pos=(425, 330))
        lost2 = TransparentText(panel, label=f"{player2} won! Score: {x}", pos=(650, 330))
        lost1.SetForegroundColour(wx.Colour(1, 135, 255))
        lost2.SetForegroundColour(wx.RED)
        lost1.SetFont(small_font)
        lost2.SetFont(small_font)
        result_texts.extend([lost1, lost2])

    func_csv(n,round_count)

    if round_count >= 5:
        wx.CallLater(1500, show_game_over)


# Main panel
app = wx.App()
mainwin = wx.Frame(None, title="Rock Paper Scissors", size=(1920, 1080))
panel = wx.Panel(mainwin)

# Background image
try:
    bg = wx.Bitmap("./2951232.jpeg")


    def on_paint(event):
        dc = wx.PaintDC(panel)
        dc.DrawBitmap(bg, 0, 0)


    panel.Bind(wx.EVT_PAINT, on_paint)
except:
    panel.SetBackgroundColour(wx.TransparentColour)

text1 = TransparentText(panel, label="Stone Paper Scissors", pos=(500, 200))
large_font = wx.Font(19, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
text1.SetFont(large_font)
text1.SetForegroundColour(wx.Colour(171, 1, 255))

mode_text = TransparentText(panel, label="Choose Game Mode", pos=(520, 230))
medium_font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
mode_text.SetFont(medium_font)
mode_text.SetForegroundColour(wx.Colour(7, 148, 158))
result_texts.append(mode_text)


# Game mode buttons
pvp = wx.Button(panel, label="Player vs Player", size=(120, 40), pos=(480, 270))
bot_btn = wx.Button(panel, label="Player vs Bot", size=(120, 40), pos=(620, 270))
pvp.Bind(wx.EVT_BUTTON,lambda e:twoplayergame())
bot_btn.Bind(wx.EVT_BUTTON, lambda e:botgame())

# Game buttons (initially hidden)
stone = wx.Button(panel, label="Rock", size=(60, 30), pos=(480, 260))
paper = wx.Button(panel, label="Paper", size=(60, 30), pos=(560, 260))
scissors = wx.Button(panel, label="Scissors", size=(60, 30), pos=(640, 260))
Rand = wx.Button(panel, label="Random", size=(60, 30), pos=(720, 260))

stone.Bind(wx.EVT_BUTTON, stonein)
paper.Bind(wx.EVT_BUTTON, paperin)
scissors.Bind(wx.EVT_BUTTON, scissorsin)
Rand.Bind(wx.EVT_BUTTON, randomuserchoice)

# Hide game buttons initially
stone.Hide()
paper.Hide()
scissors.Hide()
Rand.Hide()

mainwin.Show()
app.MainLoop()
