import webcolors

def closest_color(requested_color):
    min_colors = {}
    for name in webcolors.names("css3"): 
        r_c, g_c, b_c = webcolors.name_to_rgb(name)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        # rd = round((r_c - requested_color[0]) ** 2, 2)
        # gd = round((g_c - requested_color[1]) ** 2, 2)
        # bd = round((b_c - requested_color[2]) ** 2, 2)
        min_colors[(rd + gd + bd)**1/2] = name
    return min_colors[min(min_colors.keys())]

def get_color_name(rgb_tuple):
    try:
        # Convert RGB to hex
        hex_value = webcolors.rgb_to_hex(rgb_tuple)
        # Get the color name directly
        return webcolors.hex_to_name(hex_value)
    except ValueError:
        # If exact match not found, find the closest color
        return closest_color(rgb_tuple)
