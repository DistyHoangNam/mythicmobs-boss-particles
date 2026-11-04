# Template catalog

All deployable templates are newly authored. `core/` is a complete directory pack; optional skill files are outside it. All `NXK_` names are ordinary local conventions. The supplied static report covers the whole tree, but no template has been run in Minecraft.

| File under assets/templates | Main entries | Behavior and context |
|---|---|---|
| `core/skills/00-palette.yml` | `NXK_FX_Embers`, `NXK_FX_DustRing`, `NXK_FX_Transition`, `NXK_FX_Debris` | Cosmetic self-targeted palette; dust/data examples |
| `core/skills/10-shapes.yml` | `NXK_FX_Ring`, `NXK_FX_Sphere`, `NXK_FX_Box`, `NXK_FX_Line`, `NXK_FX_Helix`, `NXK_FX_LineRing`, `NXK_FX_Orbital` | Cosmetic shapes; line variants need a combat target |
| `core/skills/20-projectile.yml` | `NXK_Bolt_Cast`, `_Tick`, `_Hit` | Gated launch; low-count trail; direct hit damage 4, armor defaults |
| `core/skills/30-slam.yml` | `NXK_Slam_Cast`, `NXK_FX_SlamWarning` | Moving caster-centered radius-4 warning at 0/10/20 ticks, then damage 6 at tick 30 |
| `core/skills/40-aura.yml` | `NXK_FX_Aura`, `NXK_FX_AuraTick` | Cosmetic finite self aura, 80-tick duration, 5-tick interval; cooldown 6 seconds |
| `core/skills/50-fixed-zone.yml` | `NXK_Zone_Cast`, `NXK_Zone_Tick`, `NXK_Zone_Impact` | Captures target location with a totem; radius-3 warning for 40 ticks, damage 4 at end near origin |
| `core/skills/90-showcase.yml` | `NXK_Demo_Showcase` | Short cosmetic sequence; all delays are in the same entry |
| `core/mobs/showcase.yml` | `NXK_Demo_ShowcaseMob` | Invincible husk with cleared goals/targets; right-click cosmetic showcase |
| `core/mobs/boss.yml` | `NXK_Demo_Boss` | Combat husk, 200 HP; alternates opportunities for slam and bolt via timers/shared GCD |
| `core/mobs/fixed-zone.yml` | `NXK_Demo_FixedZoneMob` | Separate 100-HP combat demo for fixed-zone placement |
| `optional/geometry.skills.yml` | `NXK_FX_Sigil`, `NXK_FX_SigilPoint`, `NXK_FX_Slash`, `NXK_FX_SlashPoint` | Cosmetic callback geometry, no damage; orientation must be checked |
| `optional/premium-parameters.skills.yml` | `NXK_Premium_Burst`, `NXK_Premium_Demo` | Premium parameter example; wrapper supplies both values; helper has no universal defaults |

The demo boss's native melee remains enabled. Timer priority and GCD can make a particular cast skip an opportunity; this is intentional, not a guaranteed alternating sequence. Moving self-centered warnings are for demonstrating execution context, not a fixed arena decal. Fixed zones use the separate totem example.

For visual-only borrowing, copy the required `NXK_FX_` helpers and callers. For a different palette, change particle/data in the helpers; do not blindly search-and-replace `p`, as its meaning is mechanic-specific. For different damage, edit gameplay callbacks separately from visual geometry.

To install optional files into the demo pack, copy selected `.skills.yml` files into its `skills/` directory. The ordinary skills-directory loader reads their YAML content; the `.skills.yml` suffix is a descriptive filename here, not the newer `files/*.skill.yml` router convention. Do not copy the optional directory wholesale.
