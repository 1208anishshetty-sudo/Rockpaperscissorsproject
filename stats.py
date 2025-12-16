import wx
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


def show_stats_dialog(parent, stats):
    """Show a wx dialog with a matplotlib bar chart of win probabilities.

    stats: dict like { 'Rock': {'trials':int, 'wins':int}, ... }
    """
    dlg = wx.Dialog(parent, title="Win Probability Stats", size=(600, 420))
    panel = wx.Panel(dlg)

    fig = Figure(figsize=(5.5, 3.5))
    ax = fig.add_subplot(111)

    choices = ['Rock', 'Paper', 'Scissors']
    trials = [stats.get(c, {}).get('trials', 0) for c in choices]
    wins = [stats.get(c, {}).get('wins', 0) for c in choices]

    # compute probabilities safely
    probs = [ (wins[i] / trials[i]) * 100 if trials[i] > 0 else 0 for i in range(len(choices)) ]

    bars = ax.bar(choices, probs, color=['#ff4d4d', '#4da6ff', '#66ff99'])
    ax.set_ylim(0, 100)
    ax.set_ylabel('Win Probability (%)')
    ax.set_title('Win Probability By Choice')

    # annotate bars
    for rect, p, t, w in zip(bars, probs, trials, wins):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2.0, height + 2, f"{p:.1f}%\n({w}/{t})", ha='center', va='bottom', fontsize=9)

    canvas = FigureCanvas(panel, -1, fig)

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(canvas, 1, wx.EXPAND | wx.ALL, 5)

    btn = wx.Button(panel, label='Close')
    btn.Bind(wx.EVT_BUTTON, lambda e: dlg.EndModal(wx.ID_OK))
    sizer.Add(btn, 0, wx.ALIGN_CENTER | wx.ALL, 8)

    panel.SetSizer(sizer)
    dlg.Centre()
    dlg.ShowModal()
    dlg.Destroy()
