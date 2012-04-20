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
from Tkinter import Frame, StringVar, Radiobutton, LabelFrame, Label
from spectrum.calculations import numeric
from spectrum.calculations.groups import ClassicalGroup, SporadicGroup, AlternatingGroup, ExceptionalGroup
from spectrum.calculations.numeric import Constraints
from spectrum.gui.gui_elements import NumberBox, OptionList

__author__ = 'Daniel Lytkin'


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
        # group type selection (alternating, classical, sporadic, exceptional)
        group_type_frame = LabelFrame(self, text="Group type")
        group_type_frame.pack(expand=True, fill='x', padx=10, pady=5)

        # group type radio buttons (Alternating, Classical etc.)
        self._group_type = StringVar()
        self._type_radio_buttons = dict()
        for type in ("Alternating", "Classical", "Exceptional", "Sporadic"):
            self._type_radio_buttons[type] = Radiobutton(group_type_frame,
                variable=self._group_type, value=type, text=type)
            self._type_radio_buttons[type].pack(anchor='nw', padx=10)

        # set group type selection handler
        self._group_type.trace("w",
            lambda n, i, m: self._group_type_selection())

        # parameters for each group (degree for alternating, field and
        # dimension for classical etc.
        group_params_frame = LabelFrame(self, text="Parameters")
        group_params_frame.pack(expand=True, fill='x', padx=10, pady=5)

        # alternating
        self._alt_params = Frame(group_params_frame)
        self._alt_params.columnconfigure(1, weight=1)
        Label(self._alt_params, text="Degree").grid(sticky='w')
        self._alt_degree = NumberBox(self._alt_params,
            constraints=Constraints(min=5))
        self._alt_degree.grid(row=0, column=1, sticky='we')

        # classical
        self._clas_params = Frame(group_params_frame)
        self._clas_params.columnconfigure(1, weight=1)
        Label(self._clas_params, text="Type").grid(row=0, sticky='w')
        self._clas_type = OptionList(self._clas_params,
            values=ClassicalGroup.types())

        self._clas_type.variable.trace("w",
            lambda n, i, m: self._classical_group_type_selection())

        self._clas_type.grid(row=0, column=1, sticky='we')

        Label(self._clas_params, text="Dimension").grid(row=1, sticky='w')
        self._clas_dim = NumberBox(self._clas_params)
        self._clas_dim.grid(row=1, column=1, sticky='we')
        Label(self._clas_params, text="Field order").grid(row=2, sticky='w')
        self._clas_field = NumberBox(self._clas_params,
            constraints=Constraints(primality=numeric.PRIME_POWER))
        self._clas_field.grid(row=2, column=1, sticky='we')

        self._classical_group_type_selection()

        # exceptional
        self._ex_params = Frame(group_params_frame)
        self._ex_params.columnconfigure(1, weight=1)
        Label(self._ex_params, text="Type").grid(row=0, sticky='w')
        self._ex_type = OptionList(self._ex_params,
            values=ExceptionalGroup.types())
        self._ex_type.setvar(value=ExceptionalGroup.types()[0])
        self._ex_type.grid(row=0, column=1, sticky='we')
        Label(self._ex_params, text="Field order").grid(row=1, sticky='w')
        self._ex_field = NumberBox(self._ex_params,
            constraints=Constraints(primality=numeric.PRIME_POWER))
        self._ex_field.grid(row=1, column=1, sticky='we')

        # sporadic
        self._spor_params = Frame(group_params_frame)
        self._spor_params.columnconfigure(1, weight=1)
        Label(self._spor_params, text="Group").grid(row=0, sticky='w')
        self._sporadic_group = OptionList(self._spor_params,
            values=SporadicGroup.all_groups())
        self._sporadic_group.grid(row=0, column=1, sticky='we')

        # pack params frames
        for child_frame in group_params_frame.winfo_children():
            child_frame.pack(expand=True, fill='x', padx=10)

    @property
    def selected_group(self):
        """Returns currently selected group
        """
        if self._group_type.get() == "Alternating":
            self._alt_degree.refresh_input()
            return AlternatingGroup(int(self._alt_degree.get()))
        if self._group_type.get() == "Classical":
            self._clas_dim.refresh_input()
            self._clas_field.refresh_input()
            return ClassicalGroup(self._clas_type.variable.get(),
                int(self._clas_dim.get()), int(self._clas_field.get()))
        if self._group_type.get() == "Sporadic":
            return SporadicGroup(self._sporadic_group.variable.get())
        if self._group_type.get() == "Exceptional":
            self._ex_field.refresh_input()
            return ExceptionalGroup(self._ex_type.variable.get(),
                int(self._ex_field.get()))

    def _group_type_selection(self):
        """Process the change of selected group type
        """

        def set_visible(widget, visible):
            if visible:
                widget.pack(expand=True, fill='both', padx=10, anchor='nw')
            else:
                widget.forget()

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
