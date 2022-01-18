from . import _shared
from .control import combobox_control, knob_control
from sgui.sgqt import QGridLayout, QGroupBox


class FreqSplitter:
    """ COntrols for splitting audio by frequency """
    def __init__(
            self,
            knob_size: int,
            combobox_width: int,
            first_port: int,
            combobox_items: list,
            a_rel_callback,
            a_val_callback,
            a_port_dict,
            a_preset_mgr,
            knob_kwargs: dict={},
            title="Splitter",
        ):
        self.widget = QGroupBox(title)
        self.splitters = []
        self.layout = QGridLayout(self.widget)
        port = first_port
        self.split_count_knob = knob_control(
            knob_size,
            "Splits",
            port,
            a_rel_callback,
            a_val_callback,
            0,
            3,
            0,
            _shared.KC_INTEGER,
            a_port_dict,
            a_preset_mgr,
            knob_kwargs,
        )
        port += 1
        self.split_count_knob.add_to_grid_layout(self.layout, 0)
        self.type_combobox = combobox_control(
            64,
            "Type",
            port,
            a_rel_callback,
            a_val_callback,
            ["SVF2", "SVF4"],
            a_port_dict,
            a_preset_mgr=a_preset_mgr,
        )
        port += 1
        self.type_combobox.add_to_grid_layout(self.layout, 5)
        self.res_knob = knob_control(
            knob_size,
            "Res",
            port,
            a_rel_callback,
            a_val_callback,
            -360,
            -10,
            -120,
            _shared.KC_TENTH,
            a_port_dict,
            a_preset_mgr,
            knob_kwargs,
        )
        port += 1
        self.res_knob.add_to_grid_layout(self.layout, 10)
        x = 20
        if combobox_items:
            combobox = combobox_control(
                combobox_width,
                "Output1",
                port,
                a_rel_callback,
                a_val_callback,
                combobox_items,
                a_port_dict,
                a_preset_mgr=a_preset_mgr,
            )
            combobox.add_to_grid_layout(self.layout, x)
            port += 1
        for i in range(3):
            knob = knob_control(
                knob_size,
                f"Freq{i + 1}",
                port,
                a_rel_callback,
                a_val_callback,
                30,
                120,
                51 + (i * 24),
                _shared.KC_PITCH,
                a_port_dict,
                a_preset_mgr,
                knob_kwargs,
            )
            knob.add_to_grid_layout(self.layout,x)
            x += 1
            port += 1
            if combobox_items:
                combobox = combobox_control(
                    combobox_width,
                    f"Output{i + 2}",
                    port,
                    a_rel_callback,
                    a_val_callback,
                    combobox_items,
                    a_port_dict,
                    a_preset_mgr=a_preset_mgr,
                )
                combobox.add_to_grid_layout(self.layout, x)
                port += 1
                x += 1
        self.next_port = port

    def show_freq_knobs(self, value):
        for i, controls in zip(
            range(len(self.splitters)),
            self.splitters,
        ):
            knob, combobox = controls
            if i >= value:
                knob.control.hide()
                combobox.control.hide()
            else:
                knob.control.show()
                combobox.control.show()

