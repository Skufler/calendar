"""
    Entry point for application,
    also contains root widget
"""

import pathmagic

with pathmagic.Context():
    import sqlite3
    import calendar
    import tkinter as tk

    from datetime import datetime
    from tkinter import messagebox

    from work.scripts.app.utils.constants import BTN_CLICK
    from work.scripts.app.utils.constants import STATE_DEFAULT

    from work.scripts.app.utils.dates_util import DatesUtil
    from work.scripts.app.dao.note_dao_impl import NoteDAOImpl

    from work.scripts.app.widgets.entry_date_picker import DateEntry
    from work.scripts.app.widgets.day_info_widget import DayInfoWidget
    from work.scripts.app.widgets.notes_editor_dialog import NotesEditor

    from work.scripts.app.api.calendarific_api import CalendarificAPI


class CalendarApp:
    """
        Root widget
    """

    def __init__(self, _tk, _dao, _dates_util):
        """
        Constructor
        Initializes root widget

        :param _tk: Tkinter instance
        :param _dao: Data Access Object injection
        :param _dates_util: Dates utils injection
        """
        self._tk = _tk
        self.dao = _dao
        self.dates_util = _dates_util

        # set up frame
        self.frame = tk.Frame(self._tk)
        self.frame.grid()

        self.__editor = None
        self.__day_info_widget = None
        self.__last_retrieved_month = None
        self.jump_to_date_button = None

        self.current_year = tk.IntVar()
        self.current_year.set(datetime.today().year)

        self.current_month = tk.IntVar()
        self.current_month.set(datetime.today().month)

        self.tiles = {}
        self.widgets = {}
        self.__calendar = calendar.Calendar()
        self.__entry_date_picker = DateEntry(master=self.frame)

        self.days = tk.Frame(self.frame, width=100, height=100)
        self.days.grid(row=1, column=1)

        # set up labels/UI
        self.setup_ui()

        this_month = (
            datetime.today().month,
            datetime.today().year,
        )

        self.render_month(*this_month)

    def setup_ui(self):
        """
        Setups interface

        :return: None
        """
        previous_button = tk.Button(self.frame, text='Previous')
        previous_button.bind(
            BTN_CLICK,
            lambda _: self.swipe_month(previous=True)
        )

        next_button = tk.Button(self.frame, text='Next')
        next_button.bind(
            BTN_CLICK,
            lambda _: self.swipe_month(previous=False)
        )

        self.jump_to_date_button = tk.Button(self.frame, text='Jump to date')
        self.jump_to_date_button.bind(
            BTN_CLICK,
            lambda _: self.jump_to_date_wrapper(self.__entry_date_picker.get())
        )

        self.widgets = {
            'year': tk.Label(self.frame, textvariable=self.current_year),
            'month': tk.Label(self.frame, textvariable=self.current_month),
            'next': next_button,
            'previous': previous_button,
            'jump_to_date': self.jump_to_date_button,
            'entry_date_picker': self.__entry_date_picker
        }

        self.widgets['year'].grid(row=0, column=1)
        self.widgets['month'].grid(row=0, column=2)
        self.widgets['previous'].grid(row=2, column=0, padx=10, pady=10)
        self.widgets['next'].grid(row=2, column=2, padx=10, pady=10)
        self.widgets['jump_to_date'].grid(row=2, column=3, padx=10)
        self.widgets['entry_date_picker'].grid(row=3, column=3)

    def jump_to_date_wrapper(self, date: list):
        """
        Wraps onClick event

        :param date: passed date
        """
        self.jump_to_date(date=date)
        self.jump_to_date_button.config(relief=tk.SUNKEN)

    def jump_to_date(self, date: list):
        """
        Opens calendar in picked month and year
        or shows message box with error

        :param date: date where calendar will be opened
        :return: None
        """
        try:
            self.current_month.set(int(date[1]))
            self.current_year.set(int(date[2]))

            self.render_month(
                month=self.current_month.get(),
                year=self.current_year.get()
            )
        except ValueError:
            messagebox.showerror(
                'Error',
                'Date is not picked or is incorrect'
            )

    def render_month(self, month: int, year: int):
        """
        Render calendar month

        :param month: Specified month
        :param year: Specified year
        :return: None
        """
        # ToDo: fix namings
        this_month = self.get_calendar_for(
            month=month,
            year=year
        )

        weeks = len(this_month)
        weeks = weeks - 1 if weeks == 6 else weeks

        for week in range(weeks):
            for day in range(len(this_month[0])):
                if day == 0:
                    self.tiles[week] = {}

                _id = str(week) + '_' + str(day)

                this_day = this_month[week][day]
                day_info = self.dates_util.get_day_info(this_day)

                tile = {
                    '_id': _id,
                    'info': day_info,
                    'date': this_day,
                    'state': STATE_DEFAULT,
                    'coords': {
                        'week': week,
                        'day': day
                    },
                    'button': tk.Button(
                        self.days,
                        text=this_day.day,
                        height=2,
                        width=2,
                        fg='red' if day_info['is_holiday'] or this_day.weekday() >= 5 else 'blue'
                    ),
                }

                tile['button'].bind(
                    '<Shift-1>',
                    self.on_shift_and_click_wrapper(
                        this_day
                    )
                )
                tile['button'].bind(
                    '<Control-1>',
                    self.on_ctrl_and_click_wrapper(
                        this_day,
                        tile['info']
                    )
                )
                tile['button'].grid(row=week + 1, column=day)

                self.tiles[week][day] = tile

    def clear_calendar(self):
        """
        Destroy calendar nodes to clear up interface

        :return: None
        """
        for widget in self.days.winfo_children():
            widget.destroy()
        self.tiles = {}

    def get_calendar_for(self, month: int, year: int):
        """
            Retrieve list of lists of `datetime` objects
            for `month` of `year`
            And update `__last_retrieved_month` value

        :param month: (int) assigned month
        :param year: (int) assigned year
        :return: `list` of `datetime` objects
        """

        self.__last_retrieved_month = self.__calendar.monthdatescalendar(month=month, year=year)
        return self.__last_retrieved_month

    def on_shift_and_click_wrapper(self, day):
        """
        Wraps shift press + onClick event

        :param day: passed day
        """
        return lambda button: self.on_shift_and_click(day)

    def on_ctrl_and_click_wrapper(self, day, day_info):
        """
        Wraps CTRL press + onClick event

        :param day: passed day
        :param day_info: day info
        """
        return lambda button: self.on_ctrl_and_click(day, day_info)

    def on_shift_and_click(self, day):
        """
        Invokes wrapped functionality

        :param day: passed day
        """
        self.__editor = NotesEditor(master=self.frame, dao=self.dao, day=day)

    def on_ctrl_and_click(self, day, day_info):
        """
        Invokes wrapped functionality

        :param day: passed day
        :param day_info: day info
        """
        self.__day_info_widget = DayInfoWidget(master=self.frame, day=day, day_info=day_info)

    def swipe_month(self, previous=False):
        """
        Implements the swipe mechanism

        :param previous: if True set month to previous, otherwise to the next
        :return: None
        """
        day = datetime(month=self.current_month.get(), year=self.current_year.get(), day=1)
        month = calendar.prevmonth(month=day.month, year=day.year) \
            if previous \
            else calendar.nextmonth(month=day.month, year=day.year)

        self.current_year.set(month[0])
        self.current_month.set(month[1])

        self.clear_calendar()
        self.render_month(month=month[1], year=month[0])


def main():
    """
    Entry point

    :return: None
    """
    _ = tk.Tk()

    _.title('Calendar')
    _.resizable(0, 0)

    CalendarApp(
        _tk=_,
        _dao=NoteDAOImpl(
            connection=sqlite3.connect('..\\..\\data\\notes.db', isolation_level=None),
        ),
        _dates_util=DatesUtil(date_service=CalendarificAPI())
    )
    _.mainloop()


if __name__ == '__main__':
    main()
