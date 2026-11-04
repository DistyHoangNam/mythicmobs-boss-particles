# Particle and shape field guide

## Base emission [O04]

Set `particle`, `amount`, `hSpread`, `vSpread`, `speed`, `yOffset`, and optionally `viewDistance` deliberately. The abbreviated forms `hs`/`vs`/`y` are used in templates. Spread scatters samples; it does not define the attack radius. Speed may behave differently for particles carrying data. `directional=true` is limited to particles without extra data; validate its offsets on the actual build. Entity forward/side offsets do not work with directional mode. View distance changes visibility, not collision or damage.

For clean boundaries, begin at zero spread and speed. Some natural particle motion remains particle-specific. A one-time ring is an instant emission, not a persistent decal; repeated warnings must be scheduled explicitly.

## Small useful palette

| Intent (kit design choice) | Modern names to consider | Data requirement |
|---|---|---|
| Fire | `FLAME`, `SOUL_FIRE_FLAME`, `SMALL_FLAME` | No custom color |
| Wind/impact | `CLOUD`, `POOF`, `CRIT` | No custom color |
| Bright magic | `END_ROD`, `ELECTRIC_SPARK`, `ENCHANT` | No custom color |
| Smoke | `SMOKE`, `LARGE_SMOKE` | No custom color |
| Curse/heal | `WITCH`, `HAPPY_VILLAGER`, `HEART` | Choose their built-in appearance |
| Exact RGB warning | `DUST` | `color=#RRGGBB;size=1` |
| RGB transition | `DUST_COLOR_TRANSITION` | `color=...;color2=...;size=1` |
| Ground debris | `BLOCK` | `material=STONE` or another valid block |

Names/data classes come from the official particle index and Bukkit enum; artistic roles are this kit's suggestions. The live enum is a reference for the current server API, not proof that an older server has a particle. [O05, O06]

`DUST` documents `reddust`/`redstone` aliases; its pre-1.20.5 name was `redstone`. RGB dust uses `color` and `size`. [O07]

`DUST_COLOR_TRANSITION` takes both colors plus size. [O08] `BLOCK` takes a block material; `block_crack`/`blockcrack` are documented aliases and `block_crack` was the earlier name. [O09]

Do not pass RGB settings to FLAME and expect colored fire. Do not pass item data to a block particle. Do not invent `material=<placeholder>` support for a target build: a public request for it is not a release guarantee.

## Shape selection

| Mechanic | Use | Knobs and traps | Source |
|---|---|---|---|
| `particlering` | A circular boundary | `radius`, `points`; `amount` is per point, so start at 1 | O10 |
| `particleline` | Straight visual beam | `distanceBetween`, `maxdistance`, start/target Y offsets; `fromOrigin` changes start reference; amount is per sample | O11 |
| `particlesphere` | Shell/burst | `radius`, `amount`; no documented `points` attribute | O12 |
| `particlebox` | Box volume/shape | `radius`, `amount`; use 5.14.0 behavior, see version bug note | O13 |
| `particleorbital` | Moving orbit | `points`, `radius`, `ticks`, `interval`, rotations; **`p` is points**, spell `particle=` | O15 |
| `particlelinehelix` | Corkscrew beam | `helixlength`, `helixradius`, `helixrotation`, sample spacing; still only a visual | O16 |
| `particlelinering` | Tube-like line-ring | `ringpoints`, `ringradius`, sample spacing, line maximum distance | O28 |
| `particletornado` | Layered vortex | `duration`, `maxradius`, `height`, `interval`, `rotationspeed`, cloud particle/count; specialized slice behavior needs visual testing | O29 |
| `polygon` | Sigils/star outlines | `points`, `skip`, `scale`, `distanceBetween`; callbacks render edges/vertices | O30 |
| `slash` | Arc | `width`, `height`, `angle`, `points`, `duration`; `onPoint` renders each sample | O31 |

`particleorbital` is a particle effect; `orbital` is a projectile mechanic. Do not exchange their option sets. `p` also means polygon/slash points; shape mechanics have local alias meanings.

`ParticleEquation` is still documented as nonfunctional/WIP in the inspected page. Do not ship a fabricated equation template. Build geometry with documented shapes and callbacks instead. [O32]

## Budgeting (engineering estimates, not measured benchmarks)

- Ring emission: roughly `points × amount × targets`. A 32-point ring with amount 1 draws about 32 samples; amount 50 makes about 1,600.
- Line emission: roughly `(length / distanceBetween + 1) × amount × targets`. At 24 blocks and spacing 0.4, plan for about 61 samples per cast; exact endpoint handling is implementation-specific.
- Recurring emission: multiply per-update samples by `20 / interval` and simultaneous effects. A 3-particle trail at interval 2 is roughly 30 particles/second per projectile at 20 TPS, before viewers.
- Viewer count, packet batching, client FPS, server tick cost and visual lifetime are separate budgets. Particle bundling does not eliminate rendering cost. These estimates count sample requests, not packets.

Start with one effect and one viewer, then test representative concurrent mobs/players. Reduce count, shape density, update frequency or visibility distance based on observed load. There is no universal safe particles-per-second limit in this kit.
