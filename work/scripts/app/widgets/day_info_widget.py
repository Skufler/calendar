"""
    This dialog is used to get some interesting info about day
"""
import datetime
import tkinter as tk


class DayInfoWidget(tk.Toplevel):
    """
        Widget represents some information about day
    """

    def __init__(self, master, day: datetime.date, day_info: dict, **kwargs):
        """
              Constructor
              Initializes widget

              :param master: master widget
              :param day: given day
              :param day_info: info about day
        """
        super().__init__(master, **kwargs)

        self.grab_set()
        self.resizable(0, 0)
        self.title('Day info')

        self.lbl0 = tk.Label(self, text=str(day))
        self.lbl1 = tk.Label(self, text='Is holiday: ' + ('Yes' if day_info['is_holiday'] else 'No'))
        self.lbl2 = tk.Label(self, text=day_info['name'])
        self.lbl3 = tk.Label(self, text=day_info['description'], wraplength=500)
        self.lbl4 = tk.Label(self, text=day_info['type'])

        self.lbl0.grid(column=0, row=0)
        self.lbl1.grid(column=0, row=1)
        self.lbl2.grid(column=0, row=2)
        self.lbl3.grid(column=0, row=3)
        self.lbl4.grid(column=0, row=4)
