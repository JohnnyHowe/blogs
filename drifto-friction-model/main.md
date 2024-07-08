The only friction in the game is between the wheels and the ground. That's what this deep dive is about.

# What Is Friction?
*"the resistance that one surface or object encounters when moving over another."* -https://languages.oup.com/google-dictionary-en/ \
For car tyres, friction is what turns the energy from your wheels rotating into forward movement of the car.

When driving calmly, friction between your wheels and the road is stronger than the force the force your engine can put through the wheels.
But by overcoming this with more force (think a more powerful engine or high revs and a clutch drop) or reducing friction enough (slippery ground) the wheels will start to slide. This is what allows us to drift real cars.\
The physics of real tyres and drifting is a rabbit hole I reccommend going down, but that's not the purpose of this write up.

# What Is Friction In Drifto?
Friction is the force that makes the car feel as if it were drifting (even if it is very unrealistic).\
Since drifto isn't a simulator, we can cut some corners without having a noticable impact (in fact to make it run well on mobile we need to cut some corners).

## Per Car > Per Wheel 
Friction should apply to all wheels of the car individually, but it doesn't in Drifto. **Friction is calculated and applied to the car as a whole, rather than each individual wheel**.\
In saying that, we do take note of what surface the wheel is on (if any), but that is all.

## Directional Discrimination
A friction force should resist movement in all directions, so if you push something forward, friction pushes it backwards.\
**Drifto only cares about lateral movement** when calculating and applying friction.

### When We Don't Discriminate
If the drift angle is over 90°, we use the whole velocity of the car.\
TODO: Create GIF showing the changing friction angle

# But How Much Friction?

## The Model

## Different Cars

## Different Surfaces