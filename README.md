# Blender_Utility_Scripts
Miscellaneous utility scripts for Blender to ease my switch over from Maya

## ah_batch_exporter

Exports selected objects as separate fbx files. Parent the exportable model to an empty, and name the empty as the desired filename. The script moves the selected root objects to scene origin and exports them to the selected directory.

The tool can be found on the right side of the viewport next to the gizmo and item properties (click on the tiny arrow for the toolbar to come out)
![alt text](images/batch_exporter_menu_location.png "Batch exporter menu location")

## ah_change_grid_subdivs

This script changes the grid size with a hotkey, either doubling or halving the line spacing. 
By default the hotkeys are:
| Hotkey | Function |
| shift + NUM+ |  Increase Grid Size (Double spacing)|
| shift + NUM- |  Decrease Grid Size (Halve spacing)|
| shift + NUM0 |  Reset Grid Size |

## ah_ChangeSnapMode

Adds the option to assign hotkeys to scroll through snapping modes, or to directly jump to a specific snapping mode. Out of the box pressing control while transforming objects lets you turn on snapping, but to select the mode (e.g. vertex, grid, etc.) you need to click through a dropdown. By default none of the hotkeys are set to not overwrite any default blender behavior, so you need to assign them yourself.

## Install

1. Download any of the scripts from here and save them wherever
2. In Blender, open preferences -> add-ons and select 'Install from disk'
3. Navigate to the script you downloaded and select it
4. The addon is now installed. You can find the key binding by searching 'ah' in the blender keymap

![alt text](images/install_from_disk.png "Install addon from disk")