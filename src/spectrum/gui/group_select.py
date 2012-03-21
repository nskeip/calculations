from Tkinter import Frame, OptionMenu, StringVar, Radiobutton, Entry, LabelFrame, Label
import re
from spectrum.calculations.groups import ClassicalGroup, SporadicGroup, AlternatingGroup, ExceptionalGroup
from spectrum.calculations.numeric import Constraints

__author__ = 'Daniel Lytkin'

_non_decimal = re.compile('[^\d]+')

PRIME = 1
PRIME_POWER = 2

class NumberBox(Entry):
    """Entry box, that allows only integer text. Set primality to PRIME or
    PRIME_POWER to input primes or prime powers. Use parity=1 or -1 to input
    even or odd numbers.
    """
    # TODO: flags
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


class GroupSelect(Frame):
    """This is a widget with ability to choose specific group for further
    actions.
    """

    def __init__(self, parent=None, default_type="Classical", **kw):
        Frame.__init__(self, parent, **kw)
        self._parent = parent
        self._init_components()
        self._type_radio_buttons[default_type].select()

    def _init_components(self):
        self.columnconfigure(0, weight=1)
        # group type selection (alternating, classical, sporadic, exceptional)
        group_type_frame = LabelFrame(self, text="Group type")
        group_type_frame.grid(sticky='nesw', padx=10, pady=5)

        # group type radio buttons (Alternating, Classical etc.)
        self._group_type = StringVar()
        self._type_radio_buttons = dict()
        for type in ("Alternating", "Classical", "Exceptional", "Sporadic"):
            self._type_radio_buttons[type] = Radiobutton(group_type_frame,
                variable=self._group_type, value=type, text=type)
            # stick every control to the left
        for child_frame in group_type_frame.winfo_children():
            child_frame.grid(sticky='w', padx=10)
            # set group type selection handler
        self._group_type.trace("w",
            lambda n, i, m: self._group_type_selection())

        # parameters for each group (degree for alternating, field and
        # dimension for classical etc.
        group_params_frame = LabelFrame(self, text="Parameters")
        group_params_frame.grid(sticky='we', padx=10, pady=5)
        group_params_frame.columnconfigure(0, weight=1)

        # alternating
        self._alt_params = Frame(group_params_frame)
        Label(self._alt_params, text="Degree").grid(sticky='w')
        self._alt_degree = NumberBox(self._alt_params,
            constraints=Constraints(min=5))
        self._alt_degree.grid(row=0, column=1, sticky='w')

        # classical
        self._clas_params = Frame(group_params_frame)
        self._clas_params.columnconfigure(1, weight=1)
        Label(self._clas_params, text="Type").grid(row=0, sticky='w')
        self._clas_type = OptionList(self._clas_params,
            values=ClassicalGroup.types())

        self._clas_type.variable.trace("w",
            lambda n, i, m: self._classical_group_type_selection())

        self._clas_type.grid(row=0, column=1, sticky='w')

        Label(self._clas_params, text="Dimension").grid(row=1, sticky='w')
        self._clas_dim = NumberBox(self._clas_params)
        self._clas_dim.grid(row=1, column=1, sticky='w')
        Label(self._clas_params, text="Field order").grid(row=2, sticky='w')
        self._clas_field = NumberBox(self._clas_params,
            constraints=Constraints(primality=PRIME_POWER))
        self._clas_field.grid(row=2, column=1, sticky='w')

        self._classical_group_type_selection()

        # exceptional
        self._ex_params = Frame(group_params_frame)
        self._ex_params.columnconfigure(1, weight=1)
        Label(self._ex_params, text="Type").grid(row=0, sticky='w')
        self._ex_type = OptionList(self._ex_params,
            values=ExceptionalGroup.types())
        self._ex_type.setvar(value=ExceptionalGroup.types()[0])
        self._ex_type.grid(row=0, column=1, sticky='w')
        Label(self._ex_params, text="Field order").grid(row=1, sticky='w')
        self._ex_field = NumberBox(self._ex_params,
            constraints=Constraints(primality=PRIME_POWER))
        self._ex_field.grid(row=1, column=1, sticky='w')

        # sporadic
        self._spor_params = Frame(group_params_frame)
        Label(self._spor_params, text="Group").grid(row=0, sticky='w')
        self._sporadic_group = OptionList(self._spor_params,
            values=SporadicGroup.all_groups())
        self._sporadic_group.grid(row=0, column=1, sticky='w')

        # configure columns
        for child_frame in group_params_frame.winfo_children():
            child_frame.grid(sticky='we', padx=10)
            child_frame.columnconfigure(0, weight=1)
            child_frame.columnconfigure(1, weight=2)

    @property
    def selected_group(self):
        if self._group_type.get() == "Alternating":
            return AlternatingGroup(int(self._alt_degree.get()))
        if self._group_type.get() == "Classical":
            return ClassicalGroup(self._clas_type.variable.get(),
                int(self._clas_dim.get()), int(self._clas_field.get()))
        if self._group_type.get() == "Sporadic":
            return SporadicGroup(self._sporadic_group.variable.get())
        if self._group_type.get() == "Exceptional":
            return ExceptionalGroup(self._ex_type.variable.get(),
                int(self._ex_field.get()))

    def _group_type_selection(self):
        """Process the change of selected group type
        """

        def set_visible(widget, visible):
            if visible:
                widget.grid(sticky='we')
            else:
                widget.grid_forget()

        type = self._group_type.get()
        set_visible(self._alt_params, type == "Alternating")
        set_visible(self._clas_params, type == "Classical")
        set_visible(self._spor_params, type == "Sporadic")
        set_visible(self._ex_params, type == "Exceptional")

    def _classical_group_type_selection(self):
        name = self._clas_type.variable.get()
        self._clas_dim.set_constraints(ClassicalGroup.dim_constraints(name))
        self._clas_field.set_constraints(
            ClassicalGroup.field_constraints(name))
