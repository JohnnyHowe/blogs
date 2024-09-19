# Base Score Increase
Every frame a `baseScoreIncrease` is calculated. This takes into account the speed, angle, and surface the wheels are on.
```
private float GetBaseScoreIncreaseThisFrame()
{
    if (!ShouldAwardScore()) return 0;
    return
    (
        _carController.GetDriftAngle() *            // angle
        _carController.GetVelocity().magnitude *    // speed
        GetSurfaceTypeMultiplier() *                // between 0 and 1 to take into account road type
        baseScoreMultiplier *                       // just a constant to put scores in a nice range
        Time.deltaTime                              // make this consistent across different framerates
    );
}
```
This value is multiplied by the multiplier seen next to the car and added to your score for the run.

The `ShouldAwardScore()` function returns false if the car is on road that its already travelled before - this happens when the player goes backwards. So if this is the case, the base score increase is zero.

# Multiplier
The `multiplier` is a number between 1 and 9 that is used to multiply the base score increase (why 9? because single digits make the UI easier).

When the `multiplierProgress` goes above 1, the `multiplier` increases as long as it's below the max. When it goes below `minProgressForMultiplierDecrease` (currently -0.25) it decreases.

Why not use 0 for the decrease threshold instead of `minProgressForMultiplierDecrease`?\
Using a number below zero makes puts it in the players favour a little. It means you've got a little leeway before the `multiplier` drops.

```
private void UpdateMultiplier()
{
    UpdateMultiplierProgress();

    // increase multiplier?
    if (multiplierProgress > 1 && multiplier < maxMultiplier)
    {
        multiplierProgress -= 1;
        multiplier += 1;
    }

    // decrease multiplier?
    if (multiplierProgress <= minProgressForMultiplierDecrease && multiplier > 1)
    {
        multiplierProgress += 1 - minProgressForMultiplierDecrease;
        multiplier -= 1;
    }

    multiplier = Mathf.Clamp(multiplier, 1, maxMultiplier);
    multiplierProgress = Mathf.Max(minProgressForMultiplierDecrease, multiplierProgress);
    if (multiplier == maxMultiplier) multiplierProgress = Mathf.Min(multiplierProgress, 1);
}
```

# Multiplier Progress
This is where most of the multiplier complexity lives. As stated above, this number lives between `minProgressForMultiplierDecrease` (currently -0.25) and 1.

Every frame the progress is increased proportionally to the `baseScoreIncrease`.
```
float baseScoreIncrease = GetBaseScoreIncreaseThisFrame();
float multiplierProgressChange = baseScoreIncrease * multiplierProgressIncreaseSpeed;
```

If the car is on the ground, we also decrease it proportonally to the current multiplier level so that the higher the level, the harder it is to build up higher.
```
float multiplierDecreaseFactor = multiplier * multiplierEffectOnDecrease;
float multiplierDecrease = _multiplierDecreaseMultiplier * multiplierDecreaseFactor * Time.deltaTime;
multiplierProgressChange -= multiplierDecrease;
```

Lastly, we clamp the change (to stop it going up or down too fast) and apply it.
```
multiplierProgressChange = Mathf.Clamp(
    multiplierProgressChange,
    maxMultiplierDecreasePerSecond * Time.deltaTime,
    maxMultiplierIncreasePerSecond * Time.deltaTime
);
multiplierProgress += multiplierProgressChange;
```
# Bonuses
Real brief because this system needs some more work done to it and more bonuses added.

The current two bonuses (air time and reverse drift) work by building up their own score and applying it once the action is completed (landing on ground or exiting reverse drift).

The scores they give are not linear with time. I will explain this at a later date xo.
# FAQ
**It runs every frame? So the score is framerate dependent?**

The short answer is no, it's not framerate dependent.\
By using the time between frames (`Time.deltaTime`) in some important calculations, we negate the framerate dependency.

The UFO Framerate test (https://www.testufo.com/) shows this but with distance instead of score. By multiplying the right value changes by the time between frames, we get the same result over time (even if one looks better).