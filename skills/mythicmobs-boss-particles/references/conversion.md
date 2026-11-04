# Converting skills into MythicMobs

## Preserve behavior before translating syntax

Record the source plugin/build and dependencies; event; caster; trigger; targets; origin; shape; timing units; damage rules; cooldown; repeat semantics; and cleanup. Define whether the result must match exactly or may approximate visuals. The term NXS/Hybrid alone does not establish a file format or dependency.

Translate a small complete behavior first: trigger → warning → delay → hit → recovery. Convert visuals separately from gameplay. If the source is another engine or plugin, its collision, particle speed, color encoding, coordinate system and scheduling may differ even when names look familiar.

## Mapping worksheet

| Source feature | Core MythicMobs candidate | Caveat |
|---|---|---|
| Timed mob cast | Mob `~onTimer:N` → named metaskill | Timer runs outside combat unless conditions prevent it |
| Named function | `skill{s=ID}` | Child delays do not block the parent's following lines [O03] |
| Burst | `particles` | Particle type must support supplied data [O04–O09] |
| Circular outline | `particlering` | Count per point; visual does not cause damage [O10] |
| Straight beam | `particleline` | Visual only; source ray damage needs separate collision [O11] |
| Traveling bolt | `projectile` with tick/hit/end callbacks | Hit radii and termination are explicit design choices [O14] |
| Fixed ground warning | `totem` + origin-based callbacks | Confirm capture location, termination and terrain behavior [O23] |
| Moving buff effect | Named finite `aura` | Recast, cancellation and stack behavior need a decision [O25] |
| Shared cast lock | `offgcd` + `gcd` | Apply condition to every entry that should obey it [O24] |
| Function parameters | `<skill.parameter>` via `skill{...}` | Premium path; otherwise use explicit specialized helpers [O33] |
| Addon line offsets | Rebuild with documented core geometry | Not a name-only conversion; see C03 |
| Equation drawing | Existing shapes / polygon callbacks | Current ParticleEquation page says nonfunctional [O32] |

Before Minecraft 1.20.5, `redstone` and `block_crack` are documented earlier names for current `DUST`/`BLOCK`. Prefer official aliases over an invented universal rename table. Check sound IDs separately; converting particle aliases does not update sounds or models. [O07, O09]

## Example of a deliberate modernization

The C01 source uses named projectile callbacks. Preserve that architecture, then choose lower particle counts, bounded range/duration and an explicit target policy. In the resulting hit helper, use inherited collision targets for direct damage, and `@origin` for particles. Do not replace both with `@target` merely because the source system calls its collision entity a target.

For C03's `customparticleline`, `ys`, `vd`, `hd` and `idoy` carry addon-specific behavior. The kit's `NXK_FX_Line` uses core `startYOffset`/`targetYOffset` and drops lateral/yaw adjustment. That is an acknowledged approximation, not an exact converter.

## Output a conversion ledger

For each converted entry, report: source behavior; resulting ID/file; exact/approximate/blocked status; dependency; unit conversion; and runtime evidence. Preserve missing mechanics as a documented unresolved requirement rather than silently deleting gameplay. Do not call a successful YAML parse a successful behavioral conversion.
