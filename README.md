# Panda data augmentation Blender add-on

## Blender

This addon is built and tested for Blender 3.0.0. Blender can be downloaded from: https://www.blender.org/download/
## Installation
This add-on can be installed two ways:

**1. Using Blender UI**

	 1. Download this repository as .zip and don't unpack it
	 2. Launch Blender
	 3. Go to: Edit > Preferences > Add-ons > Install..
	 4. In the file viewer window navigate to downloaded archive and press Install Add-on
	 5. Check box next to Object: Data Augmentation

 **2. By moving files**

	 1. Download this repository as .zip and unpack it
	 2. Move the whole folder to Blender addon directory (see table below)
	 3. Go to:Edit > Preferences > Add-ons
	 4. Search for Data Augmentation
	 5. Check box next to Object: Data Augmentation
| System  | Add-on directory |
|--|--|
| MacOs |`/Users/$USER/Library/Application Support/Blender/3.0/scripts/addons/` |
| Windows| `%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\3.0\scripts\addons\` |
| Linux| `$HOME/.config/blender/3.0/scripts/addons/` |

## Overwiew

This add-on aim is to simplify the process of augmenting and generating synthetic data to be used in machine learning projects. In later stages of development, this whole process will be automated and accessible from a web interface.

This add-on supports augmenting 3D models by :
 - transforms: position, rotation, and scale in a given range
 - light conditions: strength, temperature, position, rotation, and jitter in a given range

 It also supports boundinboxes generation for multiple classes and batch rendering. It is possible to add negative data, objects that will not be labeled while being visible on renders.

Apart from standard YOLO boundinbox labels, this add-on is capable of writing rotation values of objects in rotation matrix format.

There is also an option to output all values used for augmentation and generation as a single JSON file, that file can be also later loaded into the addon to repeat the augmentation process.

## Use
This add-on to work requires a specific structure of the Blender file. A pre-made blender file can be found here: [template.blend](https://pandatechnology270-my.sharepoint.com/:u:/g/personal/maciejak_panda_technology/EToPhmK2dLZLqc9Wu0-rkBoBSFXO5TckmnyaYNtll2c12g?e=lt6kKD). If runned on Linux it is recomennded to lauchn the Blender from terminal window.  Detailed tutorial is aviable at: https://pandatech.atlassian.net/wiki/spaces/PDA/pages/1544781825/Data+Augmentation+Manual


#### Notice

<sup>BBox generation is based on https://blender.stackexchange.com/a/158236 by user juniorxsound, which is based on https://blender.stackexchange.com/a/7203 by user CodeManX</sup>