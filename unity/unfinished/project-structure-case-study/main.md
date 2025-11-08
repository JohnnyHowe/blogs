# outline (drifto)

threw everything together quick
most scripts just into Scripts folder at root
some parts feature split, some type

nov 2025
big rearrange
come back to later - is it good?


# Speeding Up This Shit

## Don't Import Some Assets
[Unity has a hanful of special folder names.](https://docs.unity3d.com/6000.2/Documentation/Manual/SpecialFolders.html)\
Of these, any folder beginning with a period (".") is ignored.

So, if you've got assets that you want in the project, but don't want Unity to import, put it in one of these folders.

### Example
`.blend` files are bigger and way slower to import than many other 3D model formats.

In Drifto, I use `.fbx` files created in [Blender](https://www.blender.org/). The `.blend` files are kept in the repo for easy editing later.\
To stop Unity spending 10+ minutes importing all of these, I moved them all to a subfolder `.blend_files/...`.

I made a python script move all .blend files to hidden folders.\
For example, all .blend files in Assets/Models/Weapons gets moved to Assets/Models/Weapons/.blend_files\
https://gist.github.com/JohnnyHowe/8c88ec807e8c2b67b51b76e6b24746ad