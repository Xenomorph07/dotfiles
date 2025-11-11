# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import hook, layout, widget, bar
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.bar import Bar
from qtile_extras.widget.decorations import RectDecoration

import subprocess
import os

import fontawesome as fa

mod = "mod4"
terminal = "alacritty"

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key(
        [mod, "control"],
        "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        desc="Grow window to the left",
    ),
    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        desc="Grow window to the right",
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "r", lazy.spawn("dmenu_run"), desc="Spawn dmenu"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("amixer sset Master 5%-"),
        desc="Lower Volume by 5%",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("amixer sset Master 5%+"),
        desc="Raise Volume by 5%",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("amixer sset Master 1+ toggle"),
        desc="Mute/Unmute Volume",
    ),
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("playerctl play-pause"),
        desc="Play/Pause player",
    ),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Skip to next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Skip to previous"),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Take screenshot"),
]

groups = [
    Group("1", label=fa.icons["terminal"]),
    Group("2", label=fa.icons["firefox"]),
    Group("3", label=fa.icons["code"]),
    Group("4", label=fa.icons["folder"]),
    Group("5", label=fa.icons["github"]),
    Group("6", label=fa.icons["spotify"] + " "),
    Group("7", label=fa.icons["bars"] + " "),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

colors = [
    "#11121d",
    "#4a5057",
    "#a0a8cd",
    "#ee6d85",
    "#f6955b",
    "#d7a65f",
    "#95c561",
    "#38a89d",
    "#bb9af7",
    "#a485dd",
    "#773440",
]

layouts = [
    layout.MonadTall(
        margin=8,
        border_focus=colors[9],
        border_width=3,
        ratio=0.6,
        new_client_position="before_current",
    ),
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="UbuntuMono Nerd Font",
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()

decor_groupbox = {
    "decorations": [
        RectDecoration(
            colour=colors[8], radius=4, filled=True, padding_y=2, padding_x=3
        )
    ],
    "padding": 18,
}

decor_ram = {
    "decorations": [
        RectDecoration(
            colour=colors[2], radius=4, filled=True, padding_y=2, padding_x=3
        )
    ],
    "padding": 13,
}

decor_CPU = {
    "decorations": [
        RectDecoration(
            colour=colors[3], radius=4, filled=True, padding_y=2, padding_x=3
        )
    ],
    "padding": 13,
}

decor_battery = {
    "decorations": [
        RectDecoration(
            colour=colors[4], radius=4, filled=True, padding_y=2, padding_x=3
        )
    ],
    "padding": 13,
}

decor_Day = {
    "decorations": [
        RectDecoration(
            colour=colors[5], radius=4, filled=True, padding_y=2, padding_x=3
        )
    ],
    "padding": 13,
}

decor_Date = {
    "decorations": [
        RectDecoration(
            colour=colors[6], radius=4, filled=True, padding_y=2, padding_x=3
        )
    ],
    "padding": 13,
}

decor_Volume = {
    "decorations": [
        RectDecoration(
            colour=colors[7], radius=4, filled=True, padding_y=2, padding_x=3
        )
    ],
    "padding": 13,
}

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Memory(
                    background="#00000000",
                    foreground=colors[0],
                    measure_mem="G",
                    format=fa.icons["server"] + " {MemUsed: .2f} GB",
                    **decor_ram
                ),
                # Can also use fa.icons["microchip"], fa.icons["chart-bar"]
                # widget.CPU(format=fa.icons["microchip"]+" {freq_current}GHz {load_percent}%",**decor_wallpaper),
                widget.CPU(
                    format=fa.icons["microchip"] + "  {load_percent}%",
                    foreground=colors[0],
                    **decor_CPU
                ),
                widget.Clock(
                    format=fa.icons["calendar"] + "  %d-%m-%y %a",
                    background="#00000000",
                    foreground=colors[0],
                    **decor_Day,
                    mouse_callbacks={
                        "Button1": lazy.group["scratchpad"].dropdown_toggle("calendar")
                    }
                ),
                widget.Spacer(length=bar.STRETCH),
                widget.GroupBox(
                    highlight_method="line",
                    highlight_color="#00000000",
                    foreground=colors[6],
                    this_screen_border=colors[5],
                    this_current_screen_border=colors[5],
                    rounded=True,
                    **decor_groupbox,
                    hide_unused=False,
                    active="#000000",
                    margin_x=6,
                    borderwidth=4
                ),
                widget.Spacer(length=bar.STRETCH),
                widget.Volume(fmt="  {}", foreground=colors[0], **decor_Volume),
                # widget.Battery(
                #     full_char=fa.icons["battery-full"],
                #     empty_char=fa.icons["battery-empty"],
                #     discharge_char=fa.icons["battery-half"],
                #     charge_char=fa.icons["battery-full"] + "  " + fa.icons["bolt"],
                #     format="{char}  {percent:2.0%}",
                #     foreground=colors[0],
                #     **decor_battery
                # ),
                widget.GenPollText(
                    update_interval=60,
                    func=lambda: "{}%".format(
                        subprocess.check_output(
                            os.path.expanduser("~/.local/bin/scripts/bat_poll")
                        ).decode("utf-8")
                    ),
                    background="#00000000",
                    foreground=colors[0],
                    **decor_battery
                ),
                widget.Clock(
                    format="  %I:%M:%S %p",
                    background="#00000000",
                    foreground=colors[0],
                    **decor_Date
                ),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background="#00000000",
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True


# @hook.subscribe.startup_once
# def autostart():
#     home = os.path.expanduser("~/.config/qtile/autostart.sh")
#     subprocess.Popen([home])


auto_minimize = True
wl_input_rules = None
wmname = "LG3D"
