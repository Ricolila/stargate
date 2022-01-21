/*
This file is part of the Stargate project, Copyright Stargate Team

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
*/

#ifndef NABU_PLUGIN_H
#define NABU_PLUGIN_H

#include "audiodsp/constants.h"
#include "audiodsp/lib/amp.h"
#include "audiodsp/lib/osc_core.h"
#include "audiodsp/lib/pitch_core.h"
#include "audiodsp/lib/smoother-linear.h"
#include "audiodsp/lib/spectrum_analyzer.h"
#include "audiodsp/modules/delay/delay_plugin.h"
#include "audiodsp/modules/delay/reverb.h"
#include "audiodsp/modules/distortion/glitch_v2.h"
#include "audiodsp/modules/filter/peak_eq.h"
#include "audiodsp/modules/filter/splitter.h"
#include "audiodsp/modules/filter/svf.h"
#include "audiodsp/modules/modulation/env_follower.h"
#include "audiodsp/modules/modulation/gate.h"
#include "audiodsp/modules/multifx/multifx10knob.h"
#include "plugin.h"
#include "compiler.h"

// The index of the main output
#define NABU_MAIN_OUT MULTIFX10_MAX_FX_COUNT
// All types of controls
#define NABU_CONTROLS_PER_FX 15
#define NABU_SLOW_INDEX_ITERATIONS 30

#define NABU_FIRST_CONTROL_PORT 4

#define NABU_LAST_CONTROL_PORT \
    (NABU_FIRST_CONTROL_PORT + (MULTIFX10_MAX_FX_COUNT * NABU_CONTROLS_PER_FX) - 1)

#define NABU_FIRST_SPLITTER_PORT (NABU_LAST_CONTROL_PORT + 1)
#define NABU_LAST_SPLITTER_PORT (NABU_FIRST_SPLITTER_PORT + 2 + (2 * 4) - 1)
/* must be 1 + highest value above
 * CHANGE THIS IF YOU ADD OR TAKE AWAY ANYTHING*/
#define NABU_PORT_COUNT (NABU_LAST_SPLITTER_PORT + 1)

struct NabuMonoModules {
    struct FreqSplitter splitter;
    struct MultiFX10MonoCluster fx[MULTIFX10_MAX_FX_COUNT];
    struct MultiFX10RoutingPlan routing_plan;
    struct SamplePair output;
};

struct NabuPlugin {
    char pad1[CACHE_LINE_SIZE];
    PluginData *output0;
    PluginData *output1;

    struct FreqSplitterControls splitter_controls;
    struct MultiFX10Controls controls[MULTIFX10_MAX_FX_COUNT];

    SGFLT fs;
    struct NabuMonoModules mono_modules;

    int i_slow_index;
    int is_on;

    struct MIDIEvent midi_events[200];
    int midi_event_count;
    t_plugin_event_queue atm_queue;
    int plugin_uid;
    fp_queue_message queue_func;

    SGFLT * port_table;
    t_plugin_cc_map cc_map;
    PluginDescriptor * descriptor;
    char pad2[CACHE_LINE_SIZE];
};

void v_nabu_mono_init(struct NabuMonoModules*, SGFLT, int);
PluginDescriptor *nabu_plugin_descriptor();

#endif /* NABU_PLUGIN_H */

