# Validation and server acceptance

## Offline checker

Requirements: Python 3.10+ and PyYAML 6.0.3. Install `scripts/requirements.txt` in a virtual environment if needed. From this skill folder:

```text
python -m pip install -r scripts/requirements.txt
python scripts/validate_templates.py --root assets/templates --report validation.json
python scripts/test_validator.py
```

The checker parses real YAML with duplicate-key rejection; checks names, skill/mob structure, mechanic/attribute allowlists for the kit's subset, positive sampling values, balanced parameter groups, callback references and template triggers; and rejects the documented nonfunctional mechanic. It checks data requirements for the included particle palette. It does not implement MythicMobs, resolve placeholders, simulate time/collisions, validate all mob options, check licensing/edition entitlement or certify performance. Dynamic values in the Premium example are identified, not evaluated.

Unknown syntax fails the subset check: that means **unsupported by this checker**, not necessarily invalid MythicMobs. When checking a converted third-party pack, use real YAML parsing plus supported checks and extend the checker only from reliable documentation. Multiple copies of the same definitions across deployment paths are not intended: install each definition once.

`validation-report.json` at the kit root records the actual build run; `runtime_tested` is false. The regression suite mutates copied templates in temporary directories and verifies meaningful failures (duplicate key, missing callback, bad particle data, invalid sample spacing, unsupported mechanic/attribute, missing brace, forbidden trigger and ID collision).

## Server acceptance (not executed during kit creation)

1. Use a test server matching your intended exact versions. Record `/mm version`, Minecraft/Paper build, Java version, edition and addons. Back up destination configs before merging.
2. Copy **only** `assets/templates/core/` as `plugins/MythicMobs/packs/nxk_demo/`. Keep its `packinfo.yml`, `mobs/` and `skills/` layout. Or merge YAML into the installation's conventional Mobs/Skills folders, without duplicating IDs. Optional templates are separate choices.
3. Run `/mm reload` and inspect the console for YAML, mechanic, targeter, condition, callback and unknown-particle errors. A reload command returning is not sufficient evidence of a clean load. [O34]
4. As an in-game administrator, run `/mm test cast NXK_Demo_Showcase` for the short cosmetic sequence. Test `/mm test cast NXK_FX_DustRing`, `NXK_FX_Orbital` and `NXK_FX_Aura` separately. The CLI test command is player-oriented; do not assume a console has valid entity context. [O34]
5. Spawn `/mm mobs spawn NXK_Demo_Boss 1` in an isolated arena. In Survival, verify that it acquires a target and the timer casts begin only inside the configured range. Observe slam's moving center, projectile wall/entity collisions and one damage application per direct hit. The cosmetic showcase mob is `NXK_Demo_ShowcaseMob`.
6. Spawn one `NXK_Demo_FixedZoneMob` to exercise the fixed totem under combat conditions. Move away from the original warning center. Confirm that the impact stays there and only nearby players are damaged. In this file the entity center is captured at placement; the warning is not terrain-snapped. Ensure early termination does not cause an unintended immediate hit.
7. Check death/despawn during windup, aura recast, no target, changing target, multiple simultaneous casters, obstacles, vertical separation, out-of-range targets and client particle settings. For polygon/slash, inspect facing and sample density before adding damage.
8. Test representative concurrent mobs/viewers and record tick time, client FPS and network behavior. Tune the budget after observation. Remove only the demo mobs/configs you installed; do not use a global kill-all command on a shared server.

Acceptance record template:

```text
Date / Minecraft / server build / Java / MythicMobs / edition / addons:
Files installed / static report hash:
Reload warnings:
Visual center, timing, geometry and visibility:
Collision and measured damage:
Recast/death/despawn/termination:
Concurrency and client/server observations:
Outcome: pass / fail / not tested
```
