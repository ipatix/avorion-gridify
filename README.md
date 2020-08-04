# Avorion Gridify

This Python script edits ships XML files from the game [Avorion](https://www.avorion.net/) and snaps all the blocks to a specified grid.

It can help in some cases to get rid of annoying flickering lines from usually invisible inner blocks. However, due to the nature of [T-Junctions](https://wiki.ldraw.org/wiki/T-Junction) it will not always work properly and you will need a properly designed ship for that.

# Usage

Use as follows:

```
./avorion-gridify.py <grid-size> <input_ship.xml> <output_ship.xml>
```

For example, if I want to snap all blocks to a grid of 0.5, I do the following:

```
./avorion-gridify.py 0.5 myship.xml newship.xml
```
