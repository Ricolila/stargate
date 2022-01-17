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

#include "plugin.h"
#include "audiodsp/lib/amp.h"
#include "audiodsp/modules/filter/svf.h"
#include "audiodsp/modules/delay/reverb.h"
#include "plugins/nabu.h"

int NABU_AMORITIZER = 0;

void v_nabu_cleanup(PluginHandle instance)
{
    free(instance);
}

void v_nabu_set_cc_map(PluginHandle instance, char * a_msg)
{
    t_nabu *plugin = (t_nabu *)instance;
    v_generic_cc_map_set(&plugin->cc_map, a_msg);
}

void v_nabu_panic(PluginHandle instance)
{
    //t_nabu *plugin = (t_nabu*)instance;
}

void v_nabu_on_stop(PluginHandle instance)
{
    //t_nabu *plugin = (t_nabu*)instance;
}

void v_nabu_connect_buffer(
    PluginHandle instance,
    int a_index,
    SGFLT * DataLocation,
    int a_is_sidechain
){
    if(a_is_sidechain)
    {
        return;
    }
    t_nabu *plugin = (t_nabu*)instance;

    switch(a_index)
    {
        case 0:
            plugin->output0 = DataLocation;
            break;
        case 1:
            plugin->output1 = DataLocation;
            break;
        default:
            sg_assert(
                0,
                "v_nabu_connect_buffer: unknown port %i",
                a_index
            );
            break;
    }
}

void v_nabu_connect_port(
    PluginHandle instance,
    int port,
    PluginData* data
){
    t_nabu* plugin = (t_nabu*)instance;
    int fx_num, fx_port, norm_port;

    if(port >= NABU_FIRST_CONTROL_PORT && port <= NABU_LAST_CONTROL_PORT){
        norm_port = (port - NABU_FIRST_CONTROL_PORT);
        fx_num = norm_port / NABU_CONTROLS_PER_FX;
        fx_port = norm_port % NABU_CONTROLS_PER_FX;
        if(fx_port < NABU_KNOBS_PER_FX){
            plugin->controls[fx_num].knobs[fx_port] = data;
        } else if(fx_port == 10){
            plugin->controls[fx_num].route = data;
        } else if(fx_port == 11){
            plugin->controls[fx_num].type = data;
        } else if(fx_port == 12){
            plugin->controls[fx_num].dry = data;
        } else if(fx_port == 13){
            plugin->controls[fx_num].wet = data;
        } else if(fx_port == 14){
            plugin->controls[fx_num].pan = data;
        } else {
            sg_abort("Nabu: Port %i has invalid fx_port: %i", port, fx_port);
        }
        return;
    }

    //switch (port){
    //}
}

PluginHandle g_nabu_instantiate(
    PluginDescriptor * descriptor,
    int s_rate,
    fp_get_audio_pool_item_from_host a_host_audio_pool_func,
    int a_plugin_uid,
    fp_queue_message
    a_queue_func
){
    t_nabu *plugin_data;
    hpalloc((void**)&plugin_data, sizeof(t_nabu));

    plugin_data->descriptor = descriptor;
    plugin_data->fs = s_rate;
    plugin_data->plugin_uid = a_plugin_uid;
    plugin_data->queue_func = a_queue_func;

    v_nabu_mono_init(
        &plugin_data->mono_modules,
        plugin_data->fs,
        plugin_data->plugin_uid
    );

    plugin_data->i_slow_index =
        NABU_SLOW_INDEX_ITERATIONS + NABU_AMORITIZER;

    ++NABU_AMORITIZER;
    if(NABU_AMORITIZER >= NABU_SLOW_INDEX_ITERATIONS){
        NABU_AMORITIZER = 0;
    }

    plugin_data->is_on = 0;

    plugin_data->port_table = g_get_port_table(
        (void**)plugin_data,
        descriptor
    );

    v_cc_map_init(&plugin_data->cc_map);
    return (PluginHandle) plugin_data;
}

void v_nabu_load(
    PluginHandle instance,
    PluginDescriptor* Descriptor,
    char * a_file_path
){
    t_nabu *plugin_data = (t_nabu*)instance;
    generic_file_loader(
        instance,
        Descriptor,
        a_file_path,
        plugin_data->port_table,
        &plugin_data->cc_map
    );
}

void v_nabu_set_port_value(
    PluginHandle Instance,
    int a_port,
    SGFLT a_value
){
    t_nabu *plugin_data = (t_nabu*)Instance;
    plugin_data->port_table[a_port] = a_value;
}

void v_nabu_check_if_on(t_nabu *plugin_data){
    int f_i, index;

    for(f_i = 0; f_i < NABU_FX_COUNT; ++f_i){
        index = (int)(*(plugin_data->controls[f_i].type));
        plugin_data->mono_modules.fx[f_i].fx_index = index;
        plugin_data->mono_modules.fx[f_i].meta = mf10_get_meta(index);

        if(index){
            plugin_data->is_on = 1;
        }
    }
}

void v_nabu_process_midi_event(
    t_nabu * plugin_data,
    t_seq_event * a_event
){
    if (a_event->type == EVENT_CONTROLLER)
    {
        sg_assert(
            a_event->param >= 1 && a_event->param < 128,
            "v_nabu_process_midi_event: param %i out of range 1 to 128",
            a_event->param
        );

        plugin_data->midi_event_types[plugin_data->midi_event_count] =
                EVENT_CONTROLLER;
        plugin_data->midi_event_ticks[plugin_data->midi_event_count] =
                a_event->tick;
        plugin_data->midi_event_ports[plugin_data->midi_event_count] =
                a_event->param;
        plugin_data->midi_event_values[plugin_data->midi_event_count] =
                a_event->value;

        if(!plugin_data->is_on)
        {
            v_nabu_check_if_on(plugin_data);

            //Meaning that we now have set the port anyways because the
            //main loop won't be running
            if(!plugin_data->is_on)
            {
                plugin_data->port_table[plugin_data->midi_event_ports[
                        plugin_data->midi_event_count]] =
                        plugin_data->midi_event_values[
                        plugin_data->midi_event_count];
            }
        }

        ++plugin_data->midi_event_count;
    }
}

void v_nabu_run(
    PluginHandle instance,
    int sample_count,
    struct ShdsList* midi_events,
    struct ShdsList *atm_events
){
    t_nabu *plugin_data = (t_nabu*)instance;
    t_nabu_mono_modules* mm = &plugin_data->mono_modules;
    t_mf10_multi * f_fx;

    t_seq_event **events = (t_seq_event**)midi_events->data;
    int event_count = midi_events->len;

    int event_pos;
    int midi_event_pos = 0;
    plugin_data->midi_event_count = 0;

    for(event_pos = 0; event_pos < event_count; ++event_pos){
        v_nabu_process_midi_event(plugin_data, events[event_pos]);
    }

    int f_i = 0;
    int i;

    v_plugin_event_queue_reset(&plugin_data->atm_queue);

    t_seq_event * ev_tmp;
    for(f_i = 0; f_i < atm_events->len; ++f_i){
        ev_tmp = (t_seq_event*)atm_events->data[f_i];
        v_plugin_event_queue_add(
            &plugin_data->atm_queue,
            ev_tmp->type,
            ev_tmp->tick,
            ev_tmp->value,
            ev_tmp->port
        );
    }

    if(plugin_data->i_slow_index >= NABU_SLOW_INDEX_ITERATIONS){
        plugin_data->i_slow_index -= NABU_SLOW_INDEX_ITERATIONS;
        plugin_data->is_on = 0;
        v_nabu_check_if_on(plugin_data);
    } else {
        ++plugin_data->i_slow_index;
    }

    if(plugin_data->is_on){
        int i_mono_out = 0;

        while(i_mono_out < sample_count){
            while(
                midi_event_pos < plugin_data->midi_event_count
                &&
                plugin_data->midi_event_ticks[midi_event_pos] == i_mono_out
            ){
                if(
                    plugin_data->midi_event_types[midi_event_pos]
                    ==
                    EVENT_CONTROLLER
                ){
                    v_cc_map_translate(
                        &plugin_data->cc_map, plugin_data->descriptor,
                        plugin_data->port_table,
                        plugin_data->midi_event_ports[midi_event_pos],
                        plugin_data->midi_event_values[midi_event_pos]
                    );
                }
                ++midi_event_pos;
            }

            v_plugin_event_queue_atm_set(
                &plugin_data->atm_queue,
                i_mono_out,
                plugin_data->port_table)
            ;

            mm->current_sample0 = plugin_data->output0[(i_mono_out)];
            mm->current_sample1 = plugin_data->output1[(i_mono_out)];

            for(f_i = 0; f_i < NABU_FX_COUNT; ++f_i){
                if(mm->fx[f_i].fx_index){
                    f_fx = &mm->fx[f_i].mf10;
                    for(i = 0; i < mm->fx[f_i].meta.knob_count; ++i){
                        v_sml_run(
                            &mm->fx[f_i].smoothers[i],
                            *plugin_data->controls[f_i].knobs[i]
                        );
                    }

                    v_mf10_set_from_smoothers(
                        f_fx,
                        mm->fx[f_i].smoothers,
                        mm->fx[f_i].meta.knob_count
                    );

                    mm->fx[f_i].meta.run(
                        f_fx,
                        mm->current_sample0,
                        mm->current_sample1
                    );

                    plugin_data->mono_modules.current_sample0 = f_fx->output0;
                    plugin_data->mono_modules.current_sample1 = f_fx->output1;
                }
            }

            plugin_data->output0[i_mono_out] = mm->current_sample0;
            plugin_data->output1[i_mono_out] = mm->current_sample1;

            ++i_mono_out;
        }
    }
}

PluginDescriptor *nabu_plugin_descriptor(){
    int i, j, port;
    PluginDescriptor *f_result = get_plugin_descriptor(NABU_PORT_COUNT);

    port = NABU_FIRST_CONTROL_PORT;
    for(i = 0; i < NABU_FX_COUNT; ++i){
        for(j = 0; j < 10; ++j){
            set_plugin_port(f_result, port, 64.0f, 0.0f, 127.0f);
            ++port;
        }
        set_plugin_port(
            f_result,
            port,  // Route
            0.0,
            0.0,
            (SGFLT)(NABU_FX_COUNT - i + 1)
        );
        ++port;
        set_plugin_port(
            f_result,
            port,  // Type
            0.0f,
            0.0f,
            MULTIFX10KNOB_FX_COUNT
        );
        ++port;
        set_plugin_port(
            f_result,
            port,  // Dry
            0.0f,
            -400.0,
            120.
        );
        ++port;
        set_plugin_port(
            f_result,
            port,  // Wet
            0.0f,
            -400.0,
            120.
        );
        ++port;
        set_plugin_port(
            f_result,
            port,  // Pan
            0.0f,
            -100.0,
            100.
        );
        ++port;
    }

    f_result->cleanup = v_nabu_cleanup;
    f_result->connect_port = v_nabu_connect_port;
    f_result->connect_buffer = v_nabu_connect_buffer;
    f_result->instantiate = g_nabu_instantiate;
    f_result->panic = v_nabu_panic;
    f_result->load = v_nabu_load;
    f_result->set_port_value = v_nabu_set_port_value;
    f_result->set_cc_map = v_nabu_set_cc_map;

    f_result->API_Version = 1;
    f_result->configure = NULL;
    f_result->run_replacing = v_nabu_run;
    f_result->on_stop = v_nabu_on_stop;
    f_result->offline_render_prep = NULL;

    return f_result;
}


void v_nabu_mono_init(
    t_nabu_mono_modules* a_mono,
    SGFLT a_sr,
    int a_plugin_uid
){
    int f_i;
    int f_i2;

    for(f_i = 0; f_i < NABU_FX_COUNT; ++f_i){
        g_mf10_init(&a_mono->fx[f_i].mf10, a_sr, 1);
        a_mono->fx[f_i].fx_index = 0;
        a_mono->fx[f_i].meta.run = v_mf10_run_off;
        for(f_i2 = 0; f_i2 < NABU_KNOBS_PER_FX; ++f_i2){
            g_sml_init(
                &a_mono->fx[f_i].smoothers[f_i2],
                a_sr,
                127.0f,
                0.0f,
                0.1f
            );
        }
    }
}

/*
void v_nabu_destructor()
{
    if (f_result) {
        free((PluginPortDescriptor *) f_result->PortDescriptors);
        free((char **) f_result->PortNames);
        free((PluginPortRangeHint *) f_result->PortRangeHints);
        free(f_result);
    }
    if (SGDDescriptor) {
        free(SGDDescriptor);
    }
}
*/
