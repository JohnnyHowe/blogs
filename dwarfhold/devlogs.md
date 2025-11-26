# Week Starting 24/11/25

## Recipe System Refactor (Technical)
Aside from a few bug fixes, this is all behind the scenes stuff. No new features, but it will allow us to work faster.

Recipes used to be stored in code as dictionaries. They were loaded from json files and used just like that. \
This worked well initially, the flexibility dictionaries gave let us prototype the systems super fast. \
Now that DwarfHold is nearing dev done, the flexibility is making it way to easy to shoot ourselves in the foot.

The solution? A dedicated `Recipe` object.
* Keep all recipe logic in one place - easier to find
* Unit tests - ensure future changes don't break old functionality 
* Hide the internals - avoid more shotgun surgery as nothing knows about *how* it works
* Hide how recipes are defined - only `Recipe` and the object that loads them care that we use JSON to define them

The `Recipe` object was pretty easy to make. Integrating it took 3 days because there were so many pieces that relied on the recipe data that weren't tested, so there were multiple rounds of just playing the game and noting new bugs. In fixing these I also had to refactor out the loading of recipes and tokens from their old modules.

The dependencies of the old system were also pretty gross.\
The loading of recipe data and runtime crafting logic were all in the same module, making circular dependencies with most of the core game systems.\
I mentioned above that I refactored this out, so none of the main systems rely on the crafting.