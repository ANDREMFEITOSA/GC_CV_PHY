import webcolors

def closest_color(requested_color):
    min_colors = {}
    for name in webcolors.names("css3"): 
        r_c, g_c, b_c = webcolors.name_to_rgb(name)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
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

# # Unique example RGB value
# unique_rgb = (123, 104, 238)  # An RGB value not directly named in CSS3 color names
# color_name = get_color_name(unique_rgb)
# print(f"The color name for RGB {unique_rgb} is {color_name}.")
