# -*- coding: utf-8 -*-
"""
This file is part of the Stargate project, Copyright Stargate Team

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

"""

from sgui.widgets import *
from sglib.lib.translate import _


NABU_FIRST_CONTROL_PORT = 4
NABU_FX0_KNOB0 = 4
NABU_FX0_KNOB1 = 5
NABU_FX0_KNOB2 = 6
NABU_FX0_COMBOBOX = 7
NABU_FX1_KNOB0 = 8
NABU_FX1_KNOB1 = 9
NABU_FX1_KNOB2 = 10
NABU_FX1_COMBOBOX = 11
NABU_FX2_KNOB0 = 12
NABU_FX2_KNOB1 = 13
NABU_FX2_KNOB2 = 14
NABU_FX2_COMBOBOX = 15
NABU_FX3_KNOB0 = 16
NABU_FX3_KNOB1 = 17
NABU_FX3_KNOB2 = 18
NABU_FX3_COMBOBOX = 19
NABU_FX4_KNOB0 = 20
NABU_FX4_KNOB1 = 21
NABU_FX4_KNOB2 = 22
NABU_FX4_COMBOBOX = 23
NABU_FX5_KNOB0 = 24
NABU_FX5_KNOB1 = 25
NABU_FX5_KNOB2 = 26
NABU_FX5_COMBOBOX = 27
NABU_FX6_KNOB0 = 28
NABU_FX6_KNOB1 = 29
NABU_FX6_KNOB2 = 30
NABU_FX6_COMBOBOX = 31
NABU_FX7_KNOB0 = 32
NABU_FX7_KNOB1 = 33
NABU_FX7_KNOB2 = 34
NABU_FX7_COMBOBOX = 35



NABU_PORT_MAP = {
    "FX0 Knob0": NABU_FX0_KNOB0,
    "FX0 Knob1": NABU_FX0_KNOB1,
    "FX0 Knob2": NABU_FX0_KNOB2,
    "FX1 Knob0": NABU_FX1_KNOB0,
    "FX1 Knob1": NABU_FX1_KNOB1,
    "FX1 Knob2": NABU_FX1_KNOB2,
    "FX2 Knob0": NABU_FX2_KNOB0,
    "FX2 Knob1": NABU_FX2_KNOB1,
    "FX2 Knob2": NABU_FX2_KNOB2,
    "FX3 Knob0": NABU_FX3_KNOB0,
    "FX3 Knob1": NABU_FX3_KNOB1,
    "FX3 Knob2": NABU_FX3_KNOB2,
    "FX4 Knob0": NABU_FX4_KNOB0,
    "FX4 Knob1": NABU_FX4_KNOB1,
    "FX4 Knob2": NABU_FX4_KNOB2,
    "FX5 Knob0": NABU_FX5_KNOB0,
    "FX5 Knob1": NABU_FX5_KNOB1,
    "FX5 Knob2": NABU_FX5_KNOB2,
    "FX6 Knob0": NABU_FX6_KNOB0,
    "FX6 Knob1": NABU_FX6_KNOB1,
    "FX6 Knob2": NABU_FX6_KNOB2,
    "FX7 Knob0": NABU_FX7_KNOB0,
    "FX7 Knob1": NABU_FX7_KNOB1,
    "FX7 Knob2": NABU_FX7_KNOB2,
}

STYLESHEET = """\
QWidget {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #2a2a2a, stop: 0.5 #3a3a3f, stop: 1 #2a2a2a
    );
    border: none;
}

QGroupBox#plugin_groupbox {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #060648, stop: 0.5 #0D0D4B, stop: 1 #060648
    );
    border: 2px solid #cccccc;
    color: #cccccc;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center; /* position at the top center */
    padding: 0 3px;
    background-color: #0D0D4B;
    border: 2px solid #cccccc;
}

QLabel#plugin_name_label,
QLabel#plugin_value_label {
    background: none;
    color: #cccccc;
}

QComboBox,
QPushButton#nested_combobox
{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #6a6a6a, stop: 0.5 #828282, stop: 1 #6a6a6a
    );
    border: 1px solid #222222;
    border-radius: 6px;
    color: #222222;
}

QAbstractItemView
{
    background-color: #222222;
    border: 2px solid #aaaaaa;
    selection-background-color: #cccccc;
}

QComboBox::drop-down
{
    border-bottom-right-radius: 3px;
    border-left-color: #222222;
    border-left-style: solid; /* just a single line */
    border-left-width: 0px;
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    color: #cccccc;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
}

QComboBox::down-arrow
{
    image: url({{ PLUGIN_ASSETS_DIR }}/drop-down.svg);
}

QMenu,
QMenu::item {
    background-color: #222222;
	color: #cccccc;
}

QMenu::separator
{
    height: 2px;
    background-color: #cccccc;
}
"""


class NabuPluginUI(AbstractPluginUI):
    def __init__(self, *args, **kwargs):
        AbstractPluginUI.__init__(
            self,
            *args,
            stylesheet=STYLESHEET,
            **kwargs,
        )
        self._plugin_name = "NABU"
        self.is_instrument = False
        knob_kwargs = {
            'arc_width_pct': 0.0,
            'fg_svg': os.path.join(
                util.PLUGIN_ASSETS_DIR,
                'knob-metal-3.svg',
            ),
        }

        self.preset_manager = preset_manager_widget(
            self.get_plugin_name())
        self.presets_hlayout = QHBoxLayout()
        self.presets_hlayout.addWidget(self.preset_manager.group_box)
        self.presets_hlayout.addItem(
            QSpacerItem(1, 1, QSizePolicy.Policy.Expanding),
        )
        self.spectrum_enabled = None

        self.main_hlayout = QHBoxLayout()
        self.layout.addLayout(self.main_hlayout)

        self.main_vlayout = QVBoxLayout()
        self.main_hlayout.addLayout(self.main_vlayout)
        self.main_vlayout.addLayout(self.presets_hlayout)
        self.fx_tab = QWidget()
        self.fx_tab.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self.main_vlayout.addWidget(self.fx_tab)


        self.fx_layout = QGridLayout()
        self.fx_hlayout = QHBoxLayout(self.fx_tab)
        self.fx_hlayout.addLayout(self.fx_layout)

        f_knob_size = 48

        f_port = 4
        f_column = 0
        f_row = 0
        for f_i in range(12):
            f_effect = MultiFXSingle(
                "FX{}".format(f_i + 1),
                f_port,
                self.plugin_rel_callback,
                self.plugin_val_callback,
                self.port_dict,
                self.preset_manager,
                a_knob_size=f_knob_size,
                knob_kwargs=knob_kwargs,
                fixed_height=True,
            )
            self.effects.append(f_effect)
            self.fx_layout.addWidget(f_effect.group_box, f_row, f_column)
            f_column += 1
            if f_column > 1:
                f_column = 0
                f_row += 1
            f_port += 4

        self.open_plugin_file()
        self.set_midi_learn(NABU_PORT_MAP)
