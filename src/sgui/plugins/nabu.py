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

NABU_FX_COUNT = 12

NABU_FIRST_CONTROL_PORT = 4
NABU_FIRST_FREQ_SPLITTER_PORT = NABU_FIRST_CONTROL_PORT + (NABU_FX_COUNT * 15)

def _port_map():
    port_map = {}
    port = NABU_FIRST_CONTROL_PORT
    for i in range(NABU_FX_COUNT):
        for j in range(10):
            port_map[f"FX{i + 1} Knob{j + 1}"] = port
            port += 1
        port += 5
    return port_map

NABU_PORT_MAP = _port_map()

STYLESHEET = """
QWidget {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #000000, stop: 0.5 #111111, stop: 1 #000000
    );
    border: none;
}

QGroupBox#plugin_groupbox {
    border: 2px solid #cccccc;
    color: #cccccc;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center; /* position at the top center */
    padding: 0 3px;
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
        f_knob_size = 48
        knob_kwargs = {
            'arc_width_pct': 20.,
            'arc_bg_brush': QColor("#5a5a5a"),
            'arc_brush': QColor("#5555cc"),
            'fg_svg': os.path.join(
                util.PLUGIN_ASSETS_DIR,
                'knob-metal-3.svg',
            ),
        }

        self.preset_manager = preset_manager_widget(
            self.get_plugin_name(),
        )
        self.presets_hlayout = QHBoxLayout()
        self.presets_hlayout.addWidget(self.preset_manager.group_box)
        self.presets_hlayout.addItem(
            QSpacerItem(1, 1, QSizePolicy.Policy.Expanding),
        )
        self.freq_splitter = FreqSplitter(
            f_knob_size,
            64,
            NABU_FIRST_FREQ_SPLITTER_PORT,
            [str(x + 1) for x in range(12)] + ["Out"],
            self.plugin_rel_callback,
            self.plugin_val_callback,
            self.port_dict,
            self.preset_manager,
            knob_kwargs,
        )
        self.layout.addWidget(self.freq_splitter.widget)
        self.spectrum_enabled = None

        self.fx_scrollarea = QScrollArea()
        self.fx_scrollarea.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn,
        )
        self.fx_scrollarea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
        )
        self.fx_scrollarea.setWidgetResizable(True)
        self.layout.addWidget(self.fx_scrollarea)
        self.fx_scrollarea_widget = QWidget()
        self.fx_layout = QVBoxLayout()
        self.fx_scrollarea_widget.setLayout(self.fx_layout)
        self.fx_scrollarea.setFixedHeight(500)
        self.fx_scrollarea.setWidget(self.fx_scrollarea_widget)

        f_port = 4
        for i in range(NABU_FX_COUNT):
            f_effect = MultiFX10(
                i,
                NABU_FX_COUNT,
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
            self.fx_layout.addWidget(f_effect.group_box)
            f_port += 15

        self.open_plugin_file()
        self.set_midi_learn(NABU_PORT_MAP)
