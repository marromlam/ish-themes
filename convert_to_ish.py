# load WEZ.rs by line

import numpy as np
import hjson
import json
import os
import shutil


with open("scheme_data.rs", "r") as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]

start = 0
for line in lines:
    if "Start here" in line:
        break
    start += 1

lines = lines[start + 1 :]


line = lines[0]


def parse_line(line):
    _line = line.strip("(),")
    _line = _line.replace('"\\n', "====")
    _line = _line.replace("\\n", "")
    _line = _line.replace("\\", "")
    color_name, color_conf = _line.split('", "')
    color_name = color_name.strip('"')
    color_conf = color_conf.replace(" ", "")

    color_conf, _ = color_conf.split("[colors.indexed]")
    _, color_conf = color_conf.split("[colors]")
    color_conf = color_conf.split("=")
    color_conf = [x.split("]") for x in color_conf]
    color_conf = sum(color_conf, [])
    # color_conf = [x.split("[") for x in color_conf]
    color_conf = [x for x in color_conf if x != ""]

    color_dict = {}
    for i in range(len(color_conf) // 2):
        _data = color_conf[2 * i + 1].split(",")
        _data = [d.split("[") for d in _data]
        _data = sum(_data, [])
        _data = [d for d in _data if d != ""]
        _data = [d.strip('"') for d in _data]
        _data = _data if len(_data) > 1 else _data[0]
        color_dict[color_conf[2 * i]] = _data
        # print(json.dumps(color_dict, indent=4))
    return color_name, color_dict


color_wez_dict = {}
for line in lines[:-2]:
    cname, cdata = parse_line(line)
    color_wez_dict[cname] = cdata


color_ish_dict = {}
TEMPLATE = {
    "shared": {
        "backgroundColor": "#282A36",
        "colorPaletteOverrides": [
            "#22212C",
            "#FF5555",
            "#50FA7B",
            "#F1FA8C",
            "#BD93F9",
            "#FF79C6",
            "#8BE9FD",
            "#F8F8F2",
            "#6272A4",
            "#FF6E6E",
            "#69FF94",
            "#FFFFA5",
            "#D6ACFF",
            "#FF92DF",
            "#A4FFFF",
            "#FFFFFF",
        ],
        "cursorColor": "#BD93F9",
        "foregroundColor": "#F8F8F2",
    },
    "version": 1,
}

shutil.rmtree("ish-colors", ignore_errors=True)
os.makedirs("ish-colors")
colors_without_cursor_bg = 0
for cname, cdata in color_wez_dict.items():
    # make a copy of the template
    _template = {"shared": {}}
    _template["shared"]["backgroundColor"] = cdata["background"]
    if "cursor_bg" in cdata:
        _template["shared"]["cursorColor"] = cdata["cursor_bg"]
    else:
        colors_without_cursor_bg += 1
        print(colors_without_cursor_bg)
        print("warn")
    _template["shared"]["foregroundColor"] = cdata["foreground"]
    _ansi, _brights = cdata["ansi"], cdata["brights"]
    # join the ansi and brights first the ansi[0] then the brights[0] then
    # ansi[1] then brights[1] and so on
    # _colors = []
    # for i in range(8):
    #     _colors.append(_ansi[i])
    #     _colors.append(_brights[i])
    _colors = [*_ansi, *_brights]
    _template["shared"]["colorPaletteOverrides"] = _colors
    color_ish_dict[cname] = _template
    with open(f"ish-colors/{cname}.json", "w") as cf:
        json.dump(_template, cf)


# print(str(parse_line(lines[0])))
