"""
    Widget for date input
"""
import tkinter as tk


class DateEntry(tk.Frame):
    """
        Widget for date input
    """

    def __init__(self, master, frame_look=None, **look):
        """
            Constructor
            Initializes Date Entry widget

            :param master: master widget
            :param frame_look: frame look
            :param look: look
        """
        if frame_look is None:
            frame_look = {}
        args = dict(relief=tk.SUNKEN, border=1)
        args.update(frame_look)
        tk.Frame.__init__(self, master, **args)

        args = {'relief': tk.FLAT}
        args.update(look)

        self.entry_1 = tk.Entry(self, width=2, **args)
        self.label_1 = tk.Label(self, text='/', **args)
        self.entry_2 = tk.Entry(self, width=2, **args)
        self.label_2 = tk.Label(self, text='/', **args)
        self.entry_3 = tk.Entry(self, width=4, **args)

        self.entry_1.pack(side=tk.LEFT)
        self.label_1.pack(side=tk.LEFT)
        self.entry_2.pack(side=tk.LEFT)
        self.label_2.pack(side=tk.LEFT)
        self.entry_3.pack(side=tk.LEFT)

        self.entries = [self.entry_1, self.entry_2, self.entry_3]

        self.entry_1.bind('<KeyRelease>', lambda e: self.__check(0, 2))
        self.entry_2.bind('<KeyRelease>', lambda e: self.__check(1, 2))
        self.entry_3.bind('<KeyRelease>', lambda e: self.__check(2, 4))

    @staticmethod
    def __backspace(entry):
        """
        Emulates backspace in entry

        :param entry: entry
        :return: None
        """
        count = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, count[:-1])

    def __check(self, index, size):
        """

        Checks entry for correct spelling

        :param index: index of field
        :param size: size of field

        :return: None
        """
        entry = self.entries[index]
        next_index = index + 1
        next_entry = self.entries[next_index] if next_index < len(self.entries) else None
        data = entry.get()

        if len(data) > size or not data.isdigit():
            self.__backspace(entry)
        if len(data) >= size and next_entry:
            next_entry.focus()

    def get(self):
        """
        Returns picked date

        :return: date
        """
        return [e.get() for e in self.entries]
