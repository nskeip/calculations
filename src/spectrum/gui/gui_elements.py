"""
Copyright 2012 Daniel Lytkin.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""
from Tkinter import Frame, Button, Listbox, Entry, StringVar, OptionMenu, Checkbutton, IntVar, Label, Menu, Scrollbar, LabelFrame
import re
import tkFont
from spectrum.calculations.numeric import Integer, Constraints
from spectrum.calculations.semisimple import SpectraElement
from spectrum.tools import pyperclip, tools
from spectrum.tools.tools import StringViewFormatter

__author__ = 'Daniel Lytkin'

_non_decimal = re.compile('[^\d]+')


class ApexList(Listbox):
    def __init__(self, parent, apex=None, **kw):
        if apex is None:
            apex = []
        kw.setdefault('selectmode', 'extended')
        Listbox.__init__(self, parent, **kw)
        self.set_apex(apex)
        self.bind("<Return>", lambda event: self.expand_selected())

        self._init_menu()

        self._right_click = None

    def _init_menu(self):
        self._menu = Menu(self, tearoff=0)
        self._menu.add_command(label="Copy", command=self._copy_selected)
        self._menu.add_command(label="Copy LaTeX", command=self._copy_selected_latex)
        self._menu.add_command(label="Expand", command=self.expand_selected)

        # right button on Mac and other systems
        button = '2' if tools.IS_MAC else '3'
        self.bind("<Button-{}>".format(button), self._right_click)

    def _right_click(self, event):
        self._right_click = event.x, event.y
        clicked_index = self.nearest(event.y)
        if not self.selection_includes(clicked_index):
            self.selection_clear(0, 'end')
            self.selection_set(clicked_index)
        self._menu.post(event.x_root, event.y_root)

    def _copy_selected(self):
        pyperclip.setcb(", ".join(map(self.get, self.curselection())))

    def _copy_selected_latex(self):
        def elem_latex(index):
            e = self._apex[index]
            if e.mode == StringViewFormatter.NORMAL:
                return e.str_normal()
            return e.str_latex()

        pyperclip.setcb(", ".join(map(elem_latex, self.curselection())))

    def curselection(self):
        """Return list of indices of currently selected items."""
        return [int(index) for index in Listbox.curselection(self)]

    def select_by_divisor(self, divisor):
        """Selects and entries divisible by 'divisor'."""
        self.selection_clear(0, 'end')
        for index, number in enumerate(self._apex):
            if number.object % divisor == 0:
                self.selection_set(index)

    def _update_text(self, index):
        self.delete(index)
        self.insert(index, self._apex[index])

    def reprint(self):
        """Updates list elements' text
        """
        for i in xrange(len(self._apex)):
            self._update_text(i)

    def expand(self, indices=None):
        """Sets elements with specified indices to show verbose view
        """
        prev_selection = self.curselection()
        for index in indices:
            self._apex[index].mode = StringViewFormatter.MIXED
            self._update_text(index)
        for index in prev_selection:
            self.selection_set(index)

    def expand_all(self):
        self.expand(range(len(self._apex)))

    def expand_selected(self):
        self.expand(self.curselection())

    def reset(self):
        """Resets every element back to plain integer view
        """
        for index in range(len(self._apex)):
            self._apex[index].mode = StringViewFormatter.NORMAL
            self._update_text(index)

    def set_apex(self, apex):
        """Sets apex shown in this list
        """

        def transform_number(number):
            if type(number) in (SpectraElement, Integer):
                return StringViewFormatter(number)
            return StringViewFormatter(Integer(number))

        self._apex = [transform_number(number) for number in apex]
        self._apex.sort(key=lambda e: e.object, reverse=True)
        self.delete(0, "END")
        self.insert(0, *self._apex)


class ApexListContainer(Frame):
    """This is a container for ApexList. Provides some additional buttons
    """

    def __init__(self, parent, apex=None, **kw):
        if apex is None:
            apex = []
        self._apex = apex
        Frame.__init__(self, parent, **kw)
        self._init_components()

    def _init_components(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # upper pane contains apex list
        upper_pane = Frame(self)
        upper_pane.columnconfigure(0, weight=1)
        upper_pane.rowconfigure(0, weight=1)

        self.apex_list = ApexList(upper_pane, self._apex)
        self.apex_list.grid(row=0, column=0, sticky='nesw')

        self._scrollbar_x = Scrollbar(upper_pane, command=self.apex_list.xview,
                                      orient='horizontal')
        self._scrollbar_x.grid(row=1, column=0, sticky='ews')
        self.apex_list['xscrollcommand'] = self._scrollbar_x.set
        self._scrollbar_y = Scrollbar(upper_pane, command=self.apex_list.yview)
        self._scrollbar_y.grid(row=0, column=1, sticky='nse')
        self.apex_list['yscrollcommand'] = self._scrollbar_y.set

        # panel with number search box
        search_pane = LabelFrame(self, text="Find number")

        self._search_box = NumberBox(search_pane, constraints=Constraints(min=1))
        self._search_box.pack(side='left', expand=True, fill='x')

        self._search_box_initial_bg = self._search_box['bg']
        self._search_box_alert_bg = '#ffaaaa'

        self._search_box.bind('<Return>', self._find_number)
        for event in ('<FocusIn>', '<FocusOut>', '<Key>'):
            self._search_box.bind(event, self._reset_search_box_alert)

        search_number_button = Button(search_pane, text="Find", command=self._find_number)
        search_number_button.pack()

        # buttons pane contain
        buttons_pane = Frame(self)

        self._expand_button = Button(buttons_pane, text="Expand All", command=self.apex_list.expand_all)
        self._expand_button.pack(side='left', expand=True, fill='x')

        self._reset_button = Button(buttons_pane, text="Collapse All", command=self.apex_list.reset)
        self._reset_button.pack()

        upper_pane.grid(sticky='nesw')
        search_pane.grid(row=1, sticky='nesw')
        buttons_pane.grid(row=2, sticky='nesw')

    def _find_number(self, *_):
        self._reset_search_box_alert()

        # select numbers divisible by input number
        self._search_box.refresh_input()
        self.apex_list.select_by_divisor(int(self._search_box.get()))

        # if no numbers selected, paint background of search box to red
        if not self.apex_list.curselection():
            self._search_box['bg'] = self._search_box_alert_bg

    def _reset_search_box_alert(self, *_):
        self._search_box['bg'] = self._search_box_initial_bg


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
    def __init__(self, parent, variable=None, values=None, **kwargs):
        if values is None:
            values = []
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


class IntegerView(Label):
    """This is the frame for displaying Integer with ability to factorize it.
    """

    def __init__(self, parent, integer=Integer(), **kw):
        #kw['state'] = 'disabled'
        kw.setdefault('anchor', 'nw')
        kw.setdefault('relief', 'sunken')

        kw.setdefault('width', 10)
        kw.setdefault('justify', 'left')
        self._var = StringVar()
        Label.__init__(self, parent, textvariable=self._var, **kw)
        self._integer_view = StringViewFormatter(integer)
        self._update_integer()
        self._factorization_enabled = False
        self.bind("<Configure>", self._update_width)

        self._init_menu()

    def _init_menu(self):
        self._menu = Menu(self, tearoff=0)
        self._menu.add_command(label="Copy", command=self._copy)
        self._menu.add_command(label="Copy LaTeX", command=self._copy_latex)

        # right button on Mac and other systems
        button = '2' if tools.IS_MAC else '3'
        self.bind("<Button-{}>".format(button), self._right_click)

    def _right_click(self, event):
        self._menu.post(event.x_root, event.y_root)

    def _copy(self):
        pyperclip.setcb(str(self._integer_view))

    def _copy_latex(self):
        if self._factorization_enabled:
            cb = self._integer_view.str_latex()
        else:
            cb = self._integer_view.str_normal()
        pyperclip.setcb(cb)

    def _update_width(self, event):
        self['wraplength'] = self.winfo_width() - 10

    def _update_integer(self):
        self._var.set(self._integer_view)

    @property
    def integer(self):
        return self._integer_view.object

    @integer.setter
    def integer(self, value):
        self._integer_view = StringViewFormatter(value)
        if self._factorization_enabled:
            self._integer_view.mode = StringViewFormatter.VERBOSE
        self._update_integer()

    def toggle_factorization(self, value):
        self._factorization_enabled = value
        if value:
            self._integer_view.mode = StringViewFormatter.VERBOSE
        else:
            self._integer_view.mode = StringViewFormatter.NORMAL
        self._update_integer()


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
        self._init_menu()

    def _init_menu(self):
        self._menu = Menu(self, tearoff=0)
        self._menu.add_command(label="Copy LaTeX", command=self._copy_latex)

        # right button on Mac and other systems
        button = '2' if tools.IS_MAC else '3'
        self.bind("<Button-{}>".format(button), self._right_click)

    def _right_click(self, event):
        self._menu.post(event.x_root, event.y_root)

    def _copy_latex(self):
        pyperclip.setcb(self._group.str_latex())

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