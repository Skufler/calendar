"""
    Widget for editing notes at selected day
"""
import datetime
import tkinter as tk
from tkinter import messagebox

from work.scripts.app.models.note import Note
from work.scripts.app.dao.note_dao_impl import NoteDAOImpl


class NotesEditor(tk.Toplevel):
    """
        Editor for notes
        Supports basic CRUD operations
    """

    def __init__(self, master, dao: NoteDAOImpl, day: datetime.date, **kwargs):
        """
        Constructor
        Initializes editor widget

        :param master: master widget
        :param dao: Data Access Object implementation
        :param day: given day
        """
        super().__init__(master, **kwargs)
        self.dao = dao
        self.clicked_day = day

        self.row_ids = []
        self.name_stringvar = tk.StringVar()
        self.description_stringvar = tk.StringVar()

        self.is_editing = False
        self.editing_index = -1
        self.name_entry = None
        self.description_entry = None
        self.empty_list_label = None

        self.list_notes = tk.Listbox(self, selectmode=tk.SINGLE)
        self.edit_button = tk.Button(
            self,
            text='Edit',
            command=self.edit_note
        )

        self.grab_set()
        self.resizable(0, 0)
        self.title("Add note")

        self.setup_ui()

    def setup_ui(self):
        """
        Setups Editor UI

        :return: None
        """
        self.setup_entries()
        self.setup_buttons()
        self.setup_listbox()

    def setup_entries(self):
        """
        Setup entries for note fields

        :return: None
        """
        label_name = tk.Label(self, text="Event name")
        label_name.grid(column=0, row=0, ipadx=5, pady=5, sticky=tk.W + tk.N)

        label_description = tk.Label(self, text="Event description")
        label_description.grid(column=0, row=1, ipadx=5, pady=5, sticky=tk.W + tk.S)

        self.name_entry = tk.Entry(self, width=20, textvariable=self.name_stringvar)
        self.description_entry = tk.Entry(self, width=20, textvariable=self.description_stringvar)

        self.name_entry.grid(column=1, row=0, padx=10, pady=5, sticky=tk.N)
        self.description_entry.grid(column=1, row=1, padx=10, pady=5, sticky=tk.S)

    def setup_buttons(self):
        """
        Setup buttons

        :return: None
        """
        submit_button = tk.Button(
            self,
            text='Submit',
            command=self.add_note_wrapper
        )
        submit_button.grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)

        close_button = tk.Button(
            self,
            text='Close',
            command=self.close_dialog
        )
        close_button.grid(column=2, row=2, padx=10, pady=10, sticky=tk.S)

        self.edit_button.grid(column=3, row=2, padx=10, pady=10)
        if len(self.row_ids) > 0:
            self.edit_button.grid()
        else:
            self.edit_button.grid_forget()

    def add_note_wrapper(self):
        """
        Checks if input fields contain empty strings

        :return: None
        """
        name = self.name_stringvar.get()
        description = self.description_stringvar.get()
        if self.is_not_blank(name) and self.is_not_blank(description):
            self.add_note()
        else:
            messagebox.showerror('Error', 'Input fields are empty!')

    @staticmethod
    def is_not_blank(string: str) -> bool:
        """
        Check if string is not blank

        :param string: target string
        :return True is string is not blank
        """
        return bool(string and string.strip())

    def show_dialog(self, event):
        """
        Shows deletion dialog

        :param event: automatically passed event
        :return: None
        """
        widget = event.widget

        response = messagebox.askquestion(
            'Delete Item',
            'Delete the item from list?'
        )
        if response == 'yes':
            index = self.row_ids[widget.curselection()[0]]
            self.dao.delete(_id=index)
            self.row_ids.pop(widget.curselection()[0])

            widget.delete(widget.curselection())
        self.setup_listbox()

    def setup_listbox(self):
        """
        Setup Listbox with list of notes for selected day

        :return: None
        """
        notes = self.dao.get_by_date(date=self.clicked_day)
        self.list_notes.delete(0, tk.END)
        self.row_ids = []

        if notes:
            self.list_notes.config(width=0)
            if self.empty_list_label is not None:
                self.empty_list_label.destroy()

            for item in notes:
                self.list_notes.insert(tk.END, '{} {} {}'.format(item.date, item.name, item.description))
                self.row_ids.append(item.uuid)

            self.list_notes.bind('<Double-Button-1>', self.show_dialog)
            self.list_notes.bind('<<ListboxSelect>>', lambda x: self.setup_buttons())
            self.list_notes.grid(row=0, column=2, columnspan=2, rowspan=2, padx=10, pady=5)
        else:
            self.list_notes.grid_remove()

            self.empty_list_label = tk.Label(self, text='There is no notes')
            self.empty_list_label.grid(row=0, column=2)

    def add_note(self):
        """
        Adds note to storage

        :return: None
        """
        note = Note(
            uuid=self.editing_index if self.is_editing else -1,
            date=self.clicked_day,
            name=self.name_stringvar.get(),
            description=self.description_stringvar.get()
        )

        if not self.is_editing:
            self.dao.create(note)
            self.list_notes.insert(tk.END, note)
        else:
            self.dao.update(note)
            self.is_editing = False
        self.setup_ui()

    def close_dialog(self):
        """
        Closes the window

        :return: None
        """
        self.destroy()

    def edit_note(self):
        """
        Edit selected note

        :return: None
        """
        try:
            element = self.dao.get_by_id(self.row_ids[self.list_notes.curselection()[0]])

            self.name_stringvar.set(element.name)
            self.description_stringvar.set(element.description)

            self.is_editing = True
            self.edit_button.grid_forget()
            self.editing_index = element.uuid
        except IndexError:
            pass
