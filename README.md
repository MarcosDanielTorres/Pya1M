# Pya1M
Pya1M aims to be a set of utility packages for my own game engine made using python just for fun/learning.  
Main library used: pygame

Currently there are only two packages implemented:  
- Level Editor
    - ./src/level_editor  
- GUI
    - ./src/gui

Both were made from scratch using just pygame for the graphics library.


![Alt Text](https://im2.ezgif.com/tmp/ezgif-2-18fcffe5f8d3.gif)

# Level Editor
The main purpose of this editor is to export maps in a format that can be understood in every game I do. So basically I thought of a specific square on the map 
as an object, which contains a tiles information, the texture, a boolean, a code, and the layers where it belongs (this object is called a MapSquare). TODO
Format of the map:
Every MapSquare in the map (contaning the information of a specific tile) will be saved in a csv-like format, ie: every MapSquare will be separated by a comma (See illustration below)

TODO

Current Features:
Place tiles on the grid.
undo-redo functionality.
Erase individual tiles.
Clear the entire map.
Zoom in and out.
Import tiles.
Import map.
Export map.


# GUI
TODO
 


