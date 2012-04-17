from Tkinter import Frame, Button, Listbox, Entry, StringVar, OptionMenu, Checkbutton, IntVar, Label, Menu, Scrollbar
import re
import tkFont
from spectrum.calculations.numeric import Integer, Constraints
from spectrum.tools import pyperclip
from spectrum.tools.tools import IS_MAC

__author__ = 'Daniel Lytkin'

_non_decimal = re.compile('[^\d]+')


class ApexList(Listbox):
    def __init__(self, parent, apex=list(), **kw):
        kw.setdefault('selectmode', 'extended')
        Listbox.__init__(self, parent, **kw)
        self.set_apex(apex)
        self.bind("<Return>",
            lambda event: self.factorize_selected())

        self._init_menu()

        self._right_click = None


    def _init_menu(self):
        self._menu = Menu(self, tearoff=0)
        self._menu.add_command(label="Copy", command=self._copy_one)
        self._menu.add_command(label="Copy all", command=self._copy_all)
        self._menu.add_command(label="Factorize all", command=self.factorize)

        # right button on Mac and other systems
        button = '2' if IS_MAC else '3'
        self.bind("<Button-{}>".format(button), self._right_click)

    def _right_click(self, event):
        self._right_click = event.x, event.y
        self._menu.post(event.x_root, event.y_root)

    def _copy_one(self):
        pyperclip.setcb(self.get(self.nearest(self._right_click[1])))

    def _copy_all(self):
        pyperclip.setcb(", ".join(map(str, self._apex)))

    def curselection(self):
        """Return list of indices of currently selected items."""
        return [int(index) for index in Listbox.curselection(self)]

    def _update_text(self, index):
        self.delete(index)
        self.insert(index, self._apex[index])

    def reprint(self):
        """Updates list elements' text
        """
        for i in xrange(len(self._apex)):
            self._update_text(i)

    def factorize(self, indices=None):
        """Sets elements with specified indices to show factorized view
        """
        if indices is None:
            indices = range(len(self._apex))
        for index in indices:
            self._apex[index].enable_factorization_str()
            self._update_text(index)
        if indices:
            next = max(indices) + 1
            self.see(next)
            self.selection_set(next)

    def factorize_selected(self):
        self.factorize(self.curselection())

    def reset(self):
        """Resets every element back to plain integer view
        """
        for index in range(len(self._apex)):
            self._apex[index].enable_factorization_str(False)
            self._update_text(index)

    def set_apex(self, apex):
        """Sets apex shown in this list
        """
        self._apex = [Integer(number) for number in apex]
        self._apex.sort()
        self.delete(0, "END")
        self.insert(0, *self._apex)


class ApexListContainer(Frame):
    """This is a container for ApexList. Provides some additional buttons
    """

    def __init__(self, parent, apex=list(), **kw):
        self._apex = apex
        Frame.__init__(self, parent, **kw)
        self._init_components()


    def _init_components(self):
        upper_pane = Frame(self)
        upper_pane.pack(expand=True, fill='both')

        self.apex_list = ApexList(upper_pane, self._apex)
        self.apex_list.pack(side='left', expand=True, fill='both')

        self._scrollbar = Scrollbar(upper_pane, command=self.apex_list.yview)
        self._scrollbar.pack(expand=True, fill='y')
        self.apex_list['yscrollcommand'] = self._scrollbar.set

        self._factorize_button = Button(self, text="Factorize",
            command=self.apex_list.factorize_selected)
        self._factorize_button.pack(side='left', expand=True, fill='x')

        self._reset_button = Button(self, text="Reset",
            command=self.apex_list.reset)
        self._reset_button.pack()


class NumberBox(Entry):
    """Entry box, that allows only integer text. Set primality to PRIME or
    PRIME_POWER to input primes or prime powers. Use parity=1 or -1 to input
    even or odd numbers.
    """

    def __init__(self, parent, text_variable=None, constraints=None, **kw):
        self._var = text_variable or StringVar()
        self._constraints = constraints or Constraints()
        self._var.set(1)
        self.refresh_input()

        Entry.__init__(self, parent, textvariable=self._var, width=10, **kw)
        self.bind("<FocusOut>", lambda event: self.refresh_input())

    def set_constraints(self, constraints):
        self._constraints = constraints
        self.refresh_input()

    def refresh_input(self):
        # remove any non-decimal character
        input = int(_non_decimal.sub('', self._var.get()))
        value = input

        value = self._constraints.closest_valid(value)


        #if input != value:
        # changed
        self._var.set(str(value))


    @property
    def variable(self):
        """Returns string variable associated with this widget."""
        return self._var


class OptionList(OptionMenu):
    def __init__(self, parent, variable=None, values=list(), **kwargs):
        self._var = variable or StringVar()
        OptionMenu.__init__(self, parent, self._var, *values, **kwargs)
        if values:
            self._var.set(values[0])

    @property
    def variable(self):
        return self._var


class CheckBox(Checkbutton):
    """Adds some methods to Checkbutton
    """

    def __init__(self, parent, **kw):
        self._var = IntVar()
        kw['variable'] = self._var
        Checkbutton.__init__(self, parent, **kw)

    @property
    def variable(self):
        return self._var

    def is_selected(self):
        return bool(self._var.get())


class IntegerView(Entry):
    """This is the frame for displaying Integer with ability to factorize it.
    """

    def __init__(self, parent, integer=Integer(), **kw):
        kw['state'] = 'readonly'
        self._var = StringVar()
        Entry.__init__(self, parent, textvariable=self._var, **kw)
        self._integer = integer
        self._update_indeger()
        self._factorization_enabled = False

    def _update_indeger(self):
        self._var.set(self._integer)

    @property
    def integer(self):
        return self._integer

    @integer.setter
    def integer(self, value):
        self._integer = value
        self._integer.enable_factorization_str(self._factorization_enabled)
        self._update_indeger()

    def toggle_factorization(self, value):
        self._factorization_enabled = value
        self._integer.enable_factorization_str(value)
        self._update_indeger()


class IntegerContainer(Frame):
    """This frame contains IntegerView and factorize button
    """

    def __init__(self, parent, integer=Integer(), **kw):
        Frame.__init__(self, parent, **kw)

        self._integer_view = IntegerView(self, integer)
        self._integer_view.pack(expand=True, fill='x', side='left')

        self._button = CheckBox(self, indicatoron=0, text="F",
            command=self._set_factorization)
        self._button.pack(side='left')

    def _set_factorization(self):
        self._integer_view.toggle_factorization(self._button.is_selected())


class GroupNameLabel(Label):
    """Label with group name"""

    def __init__(self, parent, group, **kw):
        self._group = group
        kw['text'] = str(group)
        #        kw.setdefault('anchor', 'w')
        kw.setdefault('font', tkFont.Font(size=20))
        Label.__init__(self, parent, **kw)


    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, group):
        self._group = group
        self['text'] = str(group)


class FrameWithCloseButton(Frame):
    """This is a frame that has Close button in top right corner
    """

    def __init__(self, parent, **kw):
        Frame.__init__(self, parent, **kw)
        self._init_button_area()


    def _init_button_area(self):
        self._button_area = Frame(self, relief='raised', bd=1)
        self._button_area.pack(expand=False, fill='x')

        self._close_button = Button(self._button_area, text='Close', bd=1,
            command=self.destroy)
        self._close_button.pack(side='right')














