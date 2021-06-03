import dearpygui
import dearpygui.core as dpg
import dearpygui.contexts as cxt
import dearpygui.simple as smpl

def print_me(sender, data):
    print(f"Menu Item: {sender}")

with cxt.window(label="Gantry bot"):
    with cxt.menu_bar():
        with cxt.menu(label="File"):
            dpg.add_menu_item(label="Load motion profile", callback=print_me)
            dpg.add_menu_item(label="Save motion profile", callback=print_me)

            with dpg.menu(label="Settings"):

                dpg.add_menu_item(label="Setting 1", callback=print_me)
                dpg.add_menu_item(label="Setting 2", callback=print_me)

smpl.start_dearpygui()