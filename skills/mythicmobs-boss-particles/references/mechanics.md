# Mechanics and execution context

These are concise operational notes, not a complete syntax specification. Source IDs resolve in [sources.md](sources.md).

## Two configuration layers

Mob YAML has an internal ID, `Type`, attributes and a `Skills` list; metaskill YAML has an internal skill ID, optional conditions/cooldown and `Skills`. Keep reusable spell logic in skills and only trigger wiring in mobs. [O18, O19]

A line generally has `mechanic{key=value;key=value} @Targeter ~onTrigger`; the trigger belongs to a mob line. Triggers are case sensitive. `~onTimer:100` is a five-second interval at 20 TPS, and can fire without combat unless guarded. Explicit triggers avoid legacy implicit activation. [O19]

The current Mob Options page warns that `NoAI: true` also prevents skill casting. For a stationary showcase that still casts, clear goals/targets and keep AI enabled; this kit also sets movement speed to zero. `Interactable: true` enables the intended right-click interaction. [O36, O37]

Metaskills inherit the targets supplied by their caller. A child line with its own targeter replaces them. `Cooldown: 8` is eight seconds for that caster. `Conditions` checks the caster, `TargetConditions` checks inherited targets, and `TriggerConditions` checks the triggering entity. A delayed child does not make its caller wait through that child's delay: put the complete ordered sequence in the same metaskill if order matters. [O03]

`delay 20` delays the following sequence by 20 ticks. A mechanic's `delay=20` schedules that mechanic alone. [O20]

## Context table

| Context | Visual location | Gameplay selection |
|---|---|---|
| Self-centered pulse | `@self` / `@SelfLocation` | `@PlayersInRadius{r=4}` around caster |
| Projectile tick/end | `@origin` | End-area damage can use `@PlayersNearOrigin{r=3}` |
| Projectile direct hit | `@origin` for impact particles | `damage{amount=4}` with inherited hit entities |
| Fixed totem | `@origin` in callbacks | `@PlayersNearOrigin{r=3}` |
| Aura on caster | `@self` in this kit | Avoid assuming every aura recipient is the caster |

`@target` is the caster's current combat target, not a synonym for the projectile's collision target. `@trigger` is the entity that caused the event, when available. `@TargetLocation` chooses a location; it cannot itself take damage. [O17, O19, O21, O22]

## Cast, tick, hit, end

`projectile` drives callbacks: `onTick` runs at `interval` ticks; `onHit` inherits collision entities; `onEnd` handles termination. Velocity is blocks/second, while duration and interval are ticks. Set maximum range and duration; choose entity/block collision explicitly. Rendering a trail does not create its hitbox. Keep single-target damage out of `onEnd` when it must apply only after an entity collision. [O14]

`totem` stays at its placed location and inherits projectile options. Its default Y offset is 1; the kit sets it to 0. A finite visual telegraph with an `onEnd` impact is useful for a fixed warning zone. End callbacks also need testing for early termination, not just normal expiry. [O23]

For shared cast locks, every relevant entry skill checks `offgcd`; `gcd{ticks=40}` sets a two-second caster lock. GCD does not automatically stop unchecked skills. Keep the lock long enough for the intended windup/recovery. [O24]

A finite `aura` can run `onTick`/`onEnd`; define its name, duration, interval and stacking/refresh policy. In this kit it is self-applied, so its tick effect deliberately follows the caster. Test death, recast, teleport and world-change behavior when adapting it. [O25]

Use `skill{s=Child}` for an ordinary call. Top-level `Skill: Child` has different reuse semantics, including disregarding the referenced skill's cooldown/conditions. `sync=true` is inherited by children and cannot be disabled lower in that tree; use it only when required by a mechanic, not as a particle performance switch. [O03, O26]

Damage is a separate mechanic. Keep armor/immunity defaults unless the design requires changing them. This kit's boss damage is intentional; the showcase and geometry templates are cosmetic. [O27]
