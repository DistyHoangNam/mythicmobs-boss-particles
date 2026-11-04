---
name: mythicmobs-boss-particles
description: Create, review, or convert MythicMobs mob, boss, metaskill, and particle YAML using bundled official documentation notes, community patterns, and checked templates. Use for MythicMobs configuration, not Java plugin development or client mods.
---

# MythicMobs boss and particle authoring

Use this local knowledge kit for repeatable MythicMobs configuration work. Research snapshot: **2026-11-05, Asia/Bangkok**; latest release verified in this snapshot: **5.14.0**. The notes are curated, not the complete wiki or a promise about later builds.

## Establish the target

Read existing files, logs, or project notes for the exact Minecraft/server implementation, MythicMobs build and edition, Java version, and installed addons. If unknown, draft using the explicitly stated assumption **MythicMobs 5.14.0 on a supported Paper server, modern particle names**, and identify this assumption in the result. Ask for the version when it changes a required feature. Do not assume an NXS/Hybrid pack or addon is a MythicMobs feature from its name alone.

Read [compatibility.md](references/compatibility.md) before selecting features. Prefer the core templates, which avoid Premium parameters, inline target conditions, custom origins, models, and addon mechanics. These are design choices, not a certification on every Free build.

## Choose the relevant material

- Particle palette, data requirements and shape selection: [particles.md](references/particles.md), then [template-catalog.md](references/template-catalog.md).
- Mob wiring, target inheritance, timers and cooldowns: [mechanics.md](references/mechanics.md).
- Maintainable boss structure and community evidence: [patterns-and-community.md](references/patterns-and-community.md).
- Converting existing YAML or another skill system: [conversion.md](references/conversion.md).
- Verification and server test procedure: [validation.md](references/validation.md).
- Auditable citations and evidence status: [sources.md](references/sources.md) and [sources.json](references/sources.json).

Read only what the task needs. Prefer these bundled notes for covered behavior; research again when the user requests current information, a newer version, an undocumented mechanic, an unknown addon, or a contradiction with observed behavior. Do not claim an offline snapshot is permanently current.

## Build or adapt

1. Start with a small template under `assets/templates/core/`; rename the `NXK_` identifiers consistently when incorporating it into an existing pack. Keep the caller, visual helpers and gameplay callbacks separate. Check collisions across the destination pack.
2. Put `~on...` triggers in mob skill lists. Keep metaskill lists free of triggers. Use numeric seconds for `Cooldown`; use numeric ticks for delay, GCD, timers and projectile/aura durations in portable templates.
3. Distinguish entity targets from locations. Projectile particle callbacks use `@origin`; direct hit damage inherits the hit entities and has no replacement `@target`. Use `@PlayersNearOrigin` for area effects around projectile/totem origins, and `@PlayersInRadius` for caster-centered effects.
4. Match the warning shape, center, timing and damage area. A ring is visual only. A beam is visual only unless a separate hit mechanic is configured. State whether the effect follows the caster, tracks an entity, or stays at a captured location.
5. Set explicit particle type, count, spread, speed and a finite duration when relevant. Use `amount=1` for ring/line point samples; increase points or decrease `distanceBetween` deliberately. For `particleorbital`, spell out `particle=` because `p` means points there. Do not invent `points` for `particlesphere`.
6. Do not emit `particleequation` as working code. Do not convert addon-specific offsets, models or placeholders by renaming the mechanic alone. Explain any approximation and unresolved dependency.

Copy only the files needed. `assets/templates/optional/` is opt-in and must not be bulk-loaded with core content. The parameter example requires Premium; the geometry example needs orientation testing. Preserve the user's existing folder convention; modern packs use lowercase `mobs/` and `skills/`.

## Validate and deliver

Run `python scripts/validate_templates.py --root assets/templates --report validation.json` with Python 3.10+ and PyYAML installed, or adapt the paths to the generated subset. This checker accepts a deliberately small dialect and is **not** MythicMobs' parser. For unsupported valid syntax, extend it from verified docs or use YAML-only checks and report the gap; never rewrite valid user configuration merely to satisfy its allowlist.

Report the exact target assumptions, changed files, dependencies, static checks, and runtime status. If there is no test server, say **YAML/static validation passed; Minecraft behavior not tested**. Include concise load/reload/cast steps from the validation reference. Do not say a skill is server-validated based on YAML parsing. Use the user's language; the package includes a Vietnamese installation guide at its root.
