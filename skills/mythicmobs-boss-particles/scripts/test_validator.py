#!/usr/bin/env python3
"""Behavioral regression tests of static-checker failures on copied templates."""
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_templates import validate


TEMPLATES = Path(__file__).resolve().parents[1] / 'assets' / 'templates'


class ValidatorTests(unittest.TestCase):
    def mutate(self, relative, old, new, expected):
        # Use the active workspace rather than a potentially restricted system temp.
        temp_root = (Path.cwd() / 'work' / 'nxk-validation-tests').resolve()
        temp_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='nxk-validation-', dir=temp_root) as folder:
            # Verify the exact cleanup target before TemporaryDirectory removes it.
            if Path(folder).resolve().parent != temp_root:
                raise RuntimeError('Temporary test directory escaped its intended root')
            copy = Path(folder) / 'templates'
            shutil.copytree(TEMPLATES, copy)
            file = copy / relative
            text = file.read_text(encoding='utf-8')
            self.assertIn(old, text)
            file.write_text(text.replace(old, new, 1), encoding='utf-8')
            report = validate(copy)
            self.assertEqual(report['status'], 'failed')
            self.assertTrue(any(expected in msg for msg in report['errors']), report['errors'])

    def test_complete_templates_pass(self):
        report = validate(TEMPLATES)
        self.assertEqual(report['errors'], [])
        self.assertGreater(report['references_checked'], 10)
        self.assertFalse(report['runtime_tested'])

    def test_duplicate_yaml_key(self):
        self.mutate('core/skills/30-slam.yml', '  Cooldown: 8', '  Cooldown: 8\n  Cooldown: 9', 'duplicate YAML key')

    def test_missing_hit_callback(self):
        self.mutate('core/skills/20-projectile.yml', 'onHit=NXK_Bolt_Hit', 'onHit=MissingImpact', 'missing skill/callback')

    def test_dust_requires_color(self):
        self.mutate('core/skills/00-palette.yml', 'color=#FF9D33;', '', 'missing particle data')

    def test_nonpositive_sampling(self):
        self.mutate('core/skills/10-shapes.yml', 'distanceBetween=0.4', 'distanceBetween=0', 'must be positive')

    def test_sphere_has_no_documented_points(self):
        self.mutate('core/skills/10-shapes.yml', 'radius=2;amount=32', 'radius=2;points=32;amount=32', 'unsupported particlesphere attributes')

    def test_orbital_alias_collision(self):
        self.mutate('core/skills/10-shapes.yml', 'particleorbital{particle=END_ROD', 'particleorbital{p=END_ROD', 'unsupported particleorbital attributes')

    def test_equation_not_working(self):
        self.mutate('core/skills/00-palette.yml', 'particles{particle=FLAME', 'particleequation{particle=FLAME', 'nonfunctional/WIP')

    def test_unbalanced_brace(self):
        self.mutate('core/skills/00-palette.yml', 'speed=0;y=0.7}', 'speed=0;y=0.7', 'unbalanced')

    def test_metaskill_trigger(self):
        self.mutate('core/skills/00-palette.yml', 'speed=0;y=0.7} @self', 'speed=0;y=0.7} @self ~onSpawn', 'triggers belong in mobs')

    def test_definition_collision(self):
        self.mutate('core/skills/00-palette.yml', 'NXK_FX_Embers:', 'NXK_FX_Ring:', 'duplicate definition')

    def test_location_cannot_take_damage(self):
        self.mutate('core/skills/50-fixed-zone.yml', 'damage{amount=4} @PlayersNearOrigin{r=3}', 'damage{amount=4} @origin', 'damage needs entity targets')

    def test_nonexistent_mechanic(self):
        self.mutate('core/skills/00-palette.yml', 'particles{particle=FLAME', 'magicdust{particle=FLAME', 'unsupported mechanic')

    def test_missing_premium_argument(self):
        self.mutate('optional/premium-parameters.skills.yml', ';count=12;spread=0.5', ';count=12', 'requires count and spread')

    def test_noai_disables_skill_casting(self):
        self.mutate('core/mobs/showcase.yml', '    MovementSpeed: 0', '    NoAI: true', 'NoAI=true prevents skill casting')


if __name__ == '__main__':
    unittest.main(verbosity=2)
