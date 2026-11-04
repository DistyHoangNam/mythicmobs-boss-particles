# Sources and evidence

Inspected **2026-11-05 (Asia/Bangkok)**. IDs link notes and templates to primary material. Official documentation establishes described interfaces; community sources establish observed design patterns only.

Release authority: Lumine on Hangar (R01/R02), corroborated by the official 5.14.0 changelog (O01). Other download channels were behind; no unofficial download mirror is used. The paper support range is an advertised range, not a tested matrix.

URLs are mutable and no Git commit was pinned. This package preserves concise observations, not page snapshots or whole manuals. All templates were newly authored and statically checked; nothing here is runtime-certified.

| ID | Source | Type | Used for |
|---|---|---|---|
| R01 | [Lumine: MythicMobs 5.14.0 release](https://hangar.papermc.io/Lumine/MythicMobs/versions/v5.14.0) | release | Published 2026-10-30; advertised Paper support range. |
| R02 | [Lumine: MythicMobs versions](https://hangar.papermc.io/Lumine/MythicMobs/versions/) | release | Latest listed release; distribution listings are not runtime tests. |
| O01 | [MythicMobs changelog](https://wiki.mythiccraft.io/mythicmobs/changelogs/Changelogs) | official | Versioned feature and bug-fix notes, through 5.14.0. |
| O02 | [Packs](https://wiki.mythiccraft.io/mythicmobs/Packs) | official | Pack layout, metadata, directory and file routing. |
| O03 | [Metaskills](https://wiki.mythiccraft.io/mythicmobs/Skills/Metaskills) | official | Conditions, cooldown, target inheritance and nested delayed execution. |
| O04 | [Particle](https://wiki.mythiccraft.io/mythicmobs/Skills/Mechanics/Particle) | official | Emission parameters, data restrictions and aliases. |
| O05 | [Particle Types](https://wiki.mythiccraft.io/mythicmobs/Skills/Mechanics/Particle/Particle-Types) | official | Particle data categories and type index. |
| O06 | [Bukkit Particle API](https://hub.spigotmc.org/javadocs/spigot/org/bukkit/Particle.html) | official-api | Live 26.3 enum; not an older-version availability guarantee. |
| O07 | [Dust](https://wiki.mythiccraft.io/mythicmobs/Skills/Mechanics/Particle/Particle-Types/Dust) | official | Dust options and pre-1.20.5 name. |
| O08 | [Dust Color Transition](https://wiki.mythiccraft.io/mythicmobs/Skills/Mechanics/Particle/Particle-Types/Dust_Color_Transition) | official | Two colors and size. |
| O09 | [Block](https://wiki.mythiccraft.io/mythicmobs/Skills/Mechanics/Particle/Particle-Types/Block) | official | Block material data and historical aliases. |
| O10 | [Particle Ring](https://wiki.mythiccraft.io/mythicmobs/Skills/Mechanics/ParticleRing) | official | Radius, points, per-point emission count. |
| O11 | [Particle Line](https://wiki.mythiccraft.io/mythicmobs/skills/mechanics/ParticleLine) | official | Sample spacing, endpoint heights, origin and maximum distance. |
| O12 | [Particle Sphere](https://wiki.mythiccraft.io/mythicmobs/skills/mechanics/ParticleSphere) | official | Radius and inherited particle parameters. |
| O13 | [Particle Box](https://wiki.mythiccraft.io/mythicmobs/skills/mechanics/ParticleBox) | official | Radius and inherited particle parameters; consult changelog for fixed behavior. |
| O14 | [Projectile](https://wiki.mythiccraft.io/mythicmobs/Skills/Mechanics/Projectile) | official | Callbacks, collision, bounded lifetime and velocity units. |
| O15 | [Particle Orbital](https://wiki.mythiccraft.io/mythicmobs/Skills/Mechanics/ParticleOrbital) | official | Orbit motion; points alias conflicts with particle shorthand. |
| O16 | [Particle Line Helix](https://wiki.mythiccraft.io/mythicmobs/skills/mechanics/ParticleLineHelix) | official | Helix line sampling and geometry. |
| O17 | [Targeters](https://wiki.mythiccraft.io/mythicmobs/Skills/Targeters) | official | Entity versus location selection and origin context. |
| O18 | [Mobs](https://wiki.mythiccraft.io/mythicmobs/Mobs/Mobs) | official | Mob configuration shape. |
| O19 | [Triggers](https://wiki.mythiccraft.io/mythicmobs/Skills/Triggers) | official | Mob-only trigger placement, timer ticks and trigger case sensitivity. |
| O20 | [Delay](https://wiki.mythiccraft.io/mythicmobs/skills/mechanics/delay) | official | Sequence delay versus per-mechanic scheduling. |
| O21 | [Players Near Origin](https://wiki.mythiccraft.io/mythicmobs/Skills/Targeters/PlayersNearOrigin) | official | Area selection around callback origin. |
| O22 | [Players In Radius](https://wiki.mythiccraft.io/mythicmobs/Skills/Targeters/PlayersInRadius) | official | Caster-centered player radius. |
| O23 | [Totem](https://wiki.mythiccraft.io/mythicmobs/skills/mechanics/totem) | official | Stationary projectile-like origin, offsets and lifetime callbacks. |
| O24 | [Globalcooldown](https://wiki.mythiccraft.io/mythicmobs/skills/mechanics/globalcooldown) | official | Caster lock in ticks; offgcd must be checked. |
| O25 | [Aura](https://wiki.mythiccraft.io/mythicmobs/Skills/Mechanics/Aura) | official | Finite aura callbacks, refresh/stack and cancellation behavior. |
| O26 | [Skill](https://wiki.mythiccraft.io/mythicmobs/Skills/Mechanics/Skill) | official | Metaskill calls, branching and inherited sync. |
| O27 | [Damage](https://wiki.mythiccraft.io/mythicmobs/Skills/Mechanics/Damage) | official | Damage amount and armor/immunity defaults. |
| O28 | [Particle Line Ring](https://wiki.mythiccraft.io/mythicmobs/Skills/Mechanics/ParticleLineRing) | official | Ring-shaped line geometry. |
| O29 | [Particle Tornado](https://wiki.mythiccraft.io/mythicmobs/skills/mechanics/ParticleTornado) | official | Vortex attributes; specialized slice semantics remain underspecified. |
| O30 | [Polygon](https://wiki.mythiccraft.io/mythicmobs/skills/mechanics/polygon) | official | Vertex/edge callbacks and star geometry. |
| O31 | [Slash](https://wiki.mythiccraft.io/mythicmobs/skills/mechanics/slash) | official | Point callback and arc geometry. |
| O32 | [Particle Equation](https://wiki.mythiccraft.io/mythicmobs/skills/mechanics/ParticleEquation) | official | Inspected current page warns WIP/nonfunctional; no working template supplied. |
| O33 | [Premium Features](https://wiki.mythiccraft.io/mythicmobs/Premium-Features) | official | Edition boundaries for parameters, placeholders and advanced features. |
| O34 | [Commands and Permissions](https://wiki.mythiccraft.io/mythicmobs/Commands-and-Permissions) | official | Version, reload, cast and mob-spawn test commands. |
| O35 | [Targetwithin](https://wiki.mythiccraft.io/mythicmobs/skills/conditions/targetwithin) | official | Distance guard on caster target. |
| O36 | [Mob Options](https://wiki.mythiccraft.io/mythicmobs/Mobs/Options) | official | NoAI disables skill casting; interaction and invincibility options. |
| O37 | [Custom AI](https://wiki.mythiccraft.io/mythicmobs/Mobs/Custom-AI) | official | Goal and target selector configuration; clear existing AI lists. |
| C01 | [SXRWahrheit / MythicMobs-Files / TestSkills.yml](https://github.com/SXRWahrheit/MythicMobs-Files/blob/main/Skills/TestSkills.yml) | community-primary | Public server config; launch/tick/hit and GCD patterns; historical dependencies remain. |
| C02 | [SXRWahrheit / MythicMobs-Files / BossSkills.yml](https://github.com/SXRWahrheit/MythicMobs-Files/blob/main/Skills/BossSkills.yml) | community-primary | Staged meteor and layered trail; legacy names and explosion not copied. |
| C03 | [Herocraft / mmCustomSkills26](https://github.com/Herocraft/mmCustomSkills26) | community-addon-primary | Historical 4.1-era addon documentation; not evidence of current core support. |
| A01 | [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) | official-host | Current discovery locations and manual skill structure. |
| A02 | [OpenAI: Save workflows as skills](https://learn.chatgpt.com/use-cases/reusable-codex-skills?translationFallback=pt-BR) | official-host | Documents user skills under .codex/skills; matches this session local catalog. |

## Community confidence boundaries

C01 and C02 are two files from one author/project, not two independent authors. C03 is a second project and a historical addon. Their public YAML is useful primary evidence for structure, but no author rank, license grant, current build compatibility or in-game result was independently verified. See [patterns-and-community.md](patterns-and-community.md) for the excerpts and adaptation decisions.

The .codex/skills installation choice reflects the actual skill catalog in this session and A02; the newer .agents/skills discovery locations are documented by A01. Choose one supported location, not duplicate installations.

