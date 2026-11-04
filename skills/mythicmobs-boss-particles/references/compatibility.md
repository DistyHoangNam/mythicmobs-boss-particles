# Version and edition compatibility

Snapshot: **2026-11-05 Asia/Bangkok**. Hangar's Lumine release list identifies **5.14.0**, published **2026-10-30**, with a displayed Paper range **1.21.1–26.3**. This advertised range does not replace testing your exact server/build. CurseForge was still showing 5.13.0; distribution channels can lag. [R01, R02]

## Documented changes relevant to this kit [O01]

| Release | Relevant change |
|---|---|
| 5.14.0 | Adds Minecraft 26.3, execution audiences, fallback to server Particle enum; fixes `particlebox` drawing a sphere and squaring count. |
| 5.13.0 | Expands numeric placeholder support including particle effects; adds pack/file dependency gates and Minecraft 26.2 support. |
| 5.12.1 | Batches particles; adds duration suffixes to cooldowns and most duration/interval fields. |
| 5.12.0 | Adds Minecraft 1.21.11/26.1.x support (26.1.x requires Java 25), aura components, and pack `files/` routing. |
| 5.11.0 | Adds 1.21.10; drops some older server versions; do not assume all 1.19/1.20 variants work. |

The kit deliberately uses unsuffixed numeric time values and conventional folders. Expanded placeholder parsing does not itself establish Free-edition entitlement.

## Support intent versus testing

| Group | Intended profile | Evidence and limits |
|---|---|---|
| Core templates | 5.14.0 + a supported modern Paper server | Attributes compared to current wiki; YAML and local references checked. **No Minecraft runtime test.** |
| Earlier 5.x | Candidate backport only | Review particle names, available attributes, aura behavior and known bugs. No blanket minimum-version claim. |
| Minecraft before 1.20.5 | Explicit port | DUST/BLOCK names changed; use documented old names/aliases and test. [O07, O09] |
| Folia | Separate runtime target | Changelog contains region-thread fixes, but this kit was not executed on Folia. |
| Premium optional example | Premium + 5.14.0 intended | Skill parameters and numeric placeholders used; verify entitlement in installed build. [O33] |
| Geometry optional example | 5.14.0 intended | Current polygon/slash attributes; verify orientation and sampling in-world. [O30, O31] |

## Dependency boundaries [O33]

Premium documentation lists skill parameters, inline target conditions, custom origins, raytracing and chain missile among restricted features. The core avoids them. Optional `premium-parameters.skills.yml` must be installed deliberately, never treated as a Free fallback.

ModelEngine, MythicCrucible, custom particle addons, resource-pack models and other skill plugins are distinct dependencies. In particular, `customparticleline` in Herocraft's historical addon is not core `particleline`. [C03]

Use lowercase `skills/` and `mobs/` in modern packs. For an existing traditional installation, preserve its `Skills/` and `Mobs/` convention. Pack `files/` with `*.skill.yml`/`*.mob.yml` routing is a newer alternative; these templates use the simpler directory layout. [O02]

## Frozen-source policy

For covered tasks on the declared profile, use this local snapshot without routine re-research. Recheck official sources for a newer build, an unsupported attribute, edition disagreement, new vanilla particles or a user request for latest behavior. Record the new date/build and test status when updating notes. Do not silently present future compatibility as already verified.
