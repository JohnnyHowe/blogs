I've realised in writing this that some terms are technically incorrect but oh well. See if you can spot what they are 👀.
I've also included snippets of code, both in psuedo code and C#. The code will always be explained, it's okay if you can't read it ❤️.
# Introduction
Alright so forget everything you know about car mechanics.

Imagine a box hovering just above the ground.

![box hovering slightly above the ground](/drifto%20handling%20images/box%20floating.png)

By pushing this up (suspension), forward (drivetrain), and sideways (friction and steering) we can create some very simple car physics.

# Suspension

# Drivetrain

# "Friction"
## Overview
Because the car is floating above the ground, Unity's internal physics engine doesn't apply any friction, that's up to us.

Main points
* only applies to the car laterally*.
* calculated once over the whole car, instead of per wheel.
* calculated using car slip angle (instead of wheel slip angle or car lateral velocity)

Usually a simplified lateral friction would be calculated using the lateral velocity. In Drifto it's instead done with the slip angle.

![lateral velocity vs slip angle](/drifto%20handling%20images/lateral%20velocity%20vs%20slip%20angle.png)

The force calculation really just boils down to a function of the slip angle that looks like this.

![friction curve shown as parabola](/drifto%20handling%20images/friction%20curve.png)

The more the car is sliding, the more friction tries to stop it sliding.
Unsurprisingly, real tires act way differently. It's an rabbit hole I suggest you go down and learn why this write up is so weird.

There are also multipliers for each car and stage, as well as the time based decay.

## Parabola? not another pandemic please
This curve here is a parabola and is calculated like this:
```
# psuedo code
friction_force_magnitude = constant_friction + linear_friction * slip_angle + squared_friction * slip_angle²
```
Here's the code copied straight from the project:
```
# c#
float frictionForceMagnitude = (
    ConstantFriction +
    FrictionWithLinearSlipAngle * unsignedSlipAngle +
    FrictionWithSlipAngleSquared * unsignedSlipAngle * unsignedSlipAngle
);
```

For reference, here's what they look like for a few cars in Drifto.

![comparing the friction curve of cars](/drifto%20handling%20images/friction%20curve%20comparison.png)

The graph is cut off at force = 40 as that's the max value for most cars.

## Car Specifics


## Stage, Ground, and Car Specifics

## Force Direction: When Friction Is Not Applied Laterally

# Steering