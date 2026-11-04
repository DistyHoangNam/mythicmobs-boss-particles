# Community evidence and maintainable boss patterns

These are public primary examples from their authors' repositories. They demonstrate techniques, not current-version certification or independently verified author seniority. The maintainability recommendations below are this kit's engineering synthesis.

## C01 — SXRWahrheit / MythicMobs-Files / TestSkills.yml

[Original file](https://github.com/SXRWahrheit/MythicMobs-Files/blob/main/Skills/TestSkills.yml), inspected 2026-11-05. The repository describes configurations used on its author's server. Its WindboltElite/FireboltElite families separate launch, trail and hit callbacks. Cast skills also show target-range checks and GCD locks. A short source excerpt:

```yaml
- effect:particles{p=cloud;amount=4;speed=0;hS=0.1;vS=0.1} @origin
```

Useful pattern: keep tick emission small, put direct damage in the hit callback, and render the trail at the moving origin. The kit's `20-projectile.yml` is newly authored with different IDs, values and explicit bounds. Do not transfer the source's unrelated Denizen expressions or large repeating meteor setup without its dependencies and a load test.

## C02 — SXRWahrheit / MythicMobs-Files / BossSkills.yml

[Original file](https://github.com/SXRWahrheit/MythicMobs-Files/blob/main/Skills/BossSkills.yml), inspected 2026-11-05. The Meteor family stages a pointer, delayed launch, layered trail and end effect. Short excerpt:

```yaml
- effect:particles{p=flame;a=30;vS=1.5;hS=1.5} @Origin
```

Useful pattern: combine a thin core with a wider secondary layer to create depth, and keep the temporary object's lifecycle visible in the design. The source includes legacy particle names, high counts and an explosion; these are reasons to modernize deliberately. The kit avoids copying its explosion or helper mob lifecycle, and instead includes a fixed totem telegraph with no temporary entity.

## C03 — Herocraft / mmCustomSkills26

[Author's addon documentation](https://github.com/Herocraft/mmCustomSkills26), inspected 2026-11-05. Its documented target is MythicMobs 4.1-era custom mechanics, not a current core-only pack. Short excerpt:

```yaml
- customparticleline{particle=reddust;amount=5;color=#feff90;ys=2.5;vd=1.0;hd=-1.0;idoy=true;distanceBetween=0.5;tyo=1.25} @pir{r=10} ~onTimer:5
```

Useful lesson: source provenance determines option meanings. This addon adds destination offsets; `vd` there must not be carried into core as an equivalent vertical offset. A core rewrite can use standard line height options, but lateral/yaw behavior needs a separate design. This excerpt belongs in documentation only; it is not included in deployable templates.

## How to turn those ideas into a maintainable pack

| Concern | Kit convention (not a required MythicMobs syntax) | Reason |
|---|---|---|
| Identifier collisions | Prefix IDs with `NXK_`; preserve exact referenced spelling | A pack can share its ID space with other content |
| File responsibility | `00-palette`, `10-shapes`, `20-projectile`, then boss entry skills | Makes ownership and dependencies easy to review |
| Entry versus helpers | Entry owns conditions/cooldown/GCD; helpers own a small visual or gameplay action | Prevents unintended repeated guards or hidden cooldowns |
| Telegraph | Define center, radius, windup, hit time and recovery together | Players should be able to understand and avoid the hit |
| Gameplay timing | Keep the ordered delay sequence in one parent | Nested delayed skills do not provide ordinary blocking function-call semantics |
| Shared locks | All mutually exclusive casts check the same GCD | Setting a lock alone does not constrain other entries |
| Impact logic | Direct hit inherits collision entities; AoE explicitly selects near origin | Avoids damaging the caster's current target at the wrong location |
| Recast and cleanup | Finite lifetimes; named auras with explicit refresh/stack policy | Repeated casts should have predictable cost |
| Long warnings | Choose fixed totem or moving caster deliberately | A snapshot marker and a live entity location are different designs |
| Addons | Isolate templates and list requirements at file level | Similar-looking mechanic names can come from different plugins |

The kit is a reusable starting point, not a compilation of purchased boss packs. No full community YAML file is redistributed. License grants were not established for these repositories during this research; brief attributed excerpts and newly authored templates avoid implying permission to redistribute the originals. If copying larger portions later, inspect the original license and obtain permission where needed.
