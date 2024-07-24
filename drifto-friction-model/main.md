The only friction in the game is between the wheels and the ground. That's what this deep dive is about.\
I don't write this as a tutorial on how to emulate friction for yourself, you can definitely treat it that way but this is kinda jank.\
This is up to date as of version Drifto 4.22.2.

# What Is Friction?
*"the resistance that one surface or object encounters when moving over another."* -https://languages.oup.com/google-dictionary-en/ \
For car tyres, friction is what turns the energy from your wheels rotating into forward movement of the car.

When driving calmly, friction between your wheels and the road is stronger than the force the force your engine can put through the wheels.
But by overcoming this with more force (think a more powerful engine or high revs and a clutch drop) or reducing friction enough (slippery ground) the wheels will start to slide. This is what allows us to drift real cars.\
The physics of real tyres and drifting is a rabbit hole I reccommend going down, but that's not the purpose of this write up.

# An Overview of How it Works in Drifto
So friction needs to work to stop the slide.

To make life easier we're going to apply friction over the whole car, instead of per wheel.\
Instead of looking at the direction each wheel is facing and the direction it's travelling, we are only considering the angle of the car as a whole.

Despite the above simplification, we do care what each wheel is touching, this allows us to change the friction when the car is on different surfaces. Grip of tarmac should not be the same as dirt.\
We are also throwing out the idea of a normal force. Usually the friction two objects experience is proportional to the force pushing them together, for car wheels and the ground this would involve the car weight and downforce. In Drifto, all we care about is whether the wheel is actually on the ground or not.
![Wheel on tarmac, grass, and in the air](images/surface%20type%20grip.png)

We're also only going to conisder lateral movement. We can get away with this as in Drifto, the player has no control over the acceleration, if they did then this would feel weird. Image having full grip when going forwards but none sideways.\
So the friction force is applied at a right angle from the direction the car is facing, in the opposite direction of velocity... most the time.\
When the drift angle is greater than 90° the direction is changed to be in opposition to the velocity.

In the gif below the real direction the car is travelling is shown in green and the friction force is shown in red.\
![GIF showing friction direction change as drift angle changes](images/friction%20force%20direction.gif)

When working out how much friction force to apply, strangely enough Drifto uses the drift angle of the entire car.\
The friction force is calculated as a quadratic function of the drift angle.
The force calculation boils down to this
```
force = constantFriction + linearFriction * driftAngle + squaredFriction * driftAngle^2
```
Where constantFriction, linearFriction, and squaredFriction are set by the car itself - this is how I make different cars feel different.
![Comparing the friction curves for different cars](images/friction%20curve%20comparison.png)
This graph can actually be seen per car on the PC version of Drifto (https://store.steampowered.com/app/2949020/Drifto_Infinite_Touge/)

# The Code
Here's the whole thing. This method is run once every physics loop. Keep reading to get some more detail.
```
private void _ApplyFriction()
{
    float slipAngle = _carController.GetVelocityAngleSigned();
    float unsignedSlipAngle = Mathf.Min(Mathf.Abs(slipAngle), Mathf.PI / 2f);

    float frictionForceMagnitude = (
        _configuration.ConstantFriction +
        _configuration.FrictionWithLinearSlipAngle * unsignedSlipAngle +
        _configuration.FrictionWithSlipAngleSquared * unsignedSlipAngle * unsignedSlipAngle
    );
    float frictionAccelerationMagnitude = Mathf.Min(frictionForceMagnitude, _configuration.MaxFriction);

    float frictionAccelerationUnsigned = frictionAccelerationMagnitude * _carController._GetWheelCurrentSurfaceTypesGripMultiplier();
    float instantFrictionAccelerationUnsigned = frictionAccelerationUnsigned * Time.fixedDeltaTime * _configuration.FrictionMultiplier;

    bool reverseDrift = Mathf.Abs(slipAngle) > 90 * Mathf.Deg2Rad;
    float driftDirection = slipAngle > 0 ? 1 : -1; // -1 = left, 1 = right
    Vector3 localHorizontalVelocity = _carController.GetVelocity() - _carController.GetVelocityInLocalDirection(transform.up);
    Vector3 globalFrictionDirection = (reverseDrift ? localHorizontalVelocity * -1 : transform.right * driftDirection).normalized;
    Vector3 instantFrictionAcceleration = instantFrictionAccelerationUnsigned * globalFrictionDirection;

    _rigidBody.velocity += ClampFriction(instantFrictionAcceleration);
}
```

## Break It Down Yo
We first need to know what the angle of the car is.\
The `unsignedSlipAngle` is just that, a value in radians telling us how much angle our drift has.
```
float slipAngle = _carController.GetVelocityAngleSigned();
float unsignedSlipAngle = Mathf.Min(Mathf.Abs(slipAngle), Mathf.PI / 2f);
```

The next chunk is really the core of how Drifto calculates the amount of friction to apply.\
All we need is 3 variables that we can set for each car (that's what `_configuration` is all about) and the drift angle.
```
float frictionForceMagnitude = (
    _configuration.ConstantFriction +
    _configuration.FrictionWithLinearSlipAngle * unsignedSlipAngle +
    _configuration.FrictionWithSlipAngleSquared * unsignedSlipAngle * unsignedSlipAngle
);
```

Each car has a maximum friction as well, but to be honest there are only 3 cars that differ from the default.
```
float frictionAccelerationMagnitude = Mathf.Min(frictionForceMagnitude, _configuration.MaxFriction);
```

This is where we take into account the different surfaces the wheels are on.\

Each car has a different grip value for each surface. On tarmac it's always 1, most cars are around on 0.5 dirt road and 0.25 off road.
`_carController._GetWheelCurrentSurfaceTypesGripMultiplier()` returns a value between 0 and 1. It is the sum of the surface grip multipliers for each wheel divided by 4.\
So if two wheels were on tarmac and one off road, the value we'd get is `(1 + 1 + 0.25 + 0.25) / 4 = 0.625`. Giving us about 63% grip.
```
float frictionAccelerationUnsigned = frictionAccelerationMagnitude * _carController._GetWheelCurrentSurfaceTypesGripMultiplier();
```

Multiplying by `Time.fixedDeltaTime` ensures that this runs consistently no matter the speed of the physics engine.\
`_configuration.FrictionMultiplier` is a janky way of me dynamically changing the friction multiplier based on other factors. For example, different stages have friction multipliers, the way that's applied will be by setting this variable.
```
float instantFrictionAccelerationUnsigned = frictionAccelerationUnsigned * Time.fixedDeltaTime * _configuration.FrictionMultiplier;
```

Okok so this chunk is what calculates the direction to apply the friction force. If we were emulating more realistic tyres this section would be replaced with the opposite of the cars current velocity along the ground.\
The gist of it is `globalFrictionDirection` equals 90 degrees from where the car is facing, in the direction opposing velocity.
Unless the drift angle is over 90 degrees, then it's set to the opposite of the car velocity.
```
bool reverseDrift = Mathf.Abs(slipAngle) > 90 * Mathf.Deg2Rad;
float driftDirection = slipAngle > 0 ? 1 : -1; // -1 = left, 1 = right
Vector3 localHorizontalVelocity = _carController.GetVelocity() - _carController.GetVelocityInLocalDirection(transform.up);
Vector3 globalFrictionDirection = (reverseDrift ? localHorizontalVelocity * -1 : transform.right * driftDirection).normalized;
Vector3 instantFrictionAcceleration = instantFrictionAccelerationUnsigned * globalFrictionDirection;
```

Lastly we actually apply the force to the car.
The `ClampFriction` method stops us applying so much friction that the car starts moving in the opposite direction.
```
_rigidBody.velocity += ClampFriction(instantFrictionAcceleration);
```
```
private Vector3 ClampFriction(Vector3 unclampedFriction)
{
    return new Vector3(
        Mathf.Clamp(unclampedFriction.x, -Mathf.Abs(_rigidBody.velocity.x), Mathf.Abs(_rigidBody.velocity.x)),
        Mathf.Clamp(unclampedFriction.y, -Mathf.Abs(_rigidBody.velocity.y), Mathf.Abs(_rigidBody.velocity.y)),
        Mathf.Clamp(unclampedFriction.z, -Mathf.Abs(_rigidBody.velocity.z), Mathf.Abs(_rigidBody.velocity.z))
    );
}
```