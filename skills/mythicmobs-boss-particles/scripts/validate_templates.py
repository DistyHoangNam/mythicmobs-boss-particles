#!/usr/bin/env python3
"""Static checks for the deliberately small NXK template dialect, not MythicMobs.

Requires Python 3.10+ and PyYAML. No network or server actions are performed.
Unknown valid Mythic syntax may fail this checker; extend from verified docs.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    raise SystemExit('Install the checker dependency: python -m pip install -r scripts/requirements.txt')


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in result
        except TypeError as exc:
            raise ValueError('YAML mapping keys must be scalar/hashable') from exc
        if duplicate:
            raise ValueError(f'duplicate YAML key: {key!r}, line {key_node.start_mark.line + 1}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

PARTICLE = set('particle amount hs vs speed y color color2 size material'.split())
LINE = set('distancebetween maxdistance startyoffset targetyoffset fromorigin'.split())
PROJECTILE = set(('ontick onhit onend velocity interval duration maxrange hradius vradius '
                  'startyoffset startfoffset targetyoffset stopatentity stopatblock '
                  'hitplayers hitnonplayers').split())
ATTRS = {
    'particles': PARTICLE,
    'particlering': PARTICLE | {'radius', 'points'},
    'particlesphere': PARTICLE | {'radius'},
    'particlebox': PARTICLE | {'radius'},
    'particleline': PARTICLE | LINE,
    'particlelinehelix': PARTICLE | LINE | {'helixlength', 'helixradius', 'helixrotation'},
    'particlelinering': PARTICLE | LINE | {'ringpoints', 'ringradius'},
    'particleorbital': PARTICLE | set('radius points ticks interval offsety'.split()),
    'projectile': PROJECTILE,
    'totem': PROJECTILE | {'yoffset'},
    'skill': {'s', 'count', 'spread'},  # count/spread are the optional template's own interface
    'gcd': {'ticks'},
    'damage': {'amount'},
    'aura': set(('auraname ontick onend duration interval maxstacks refreshduration '
                 'cancelondeath canceloncasterdeath cancelonchangeworld').split()),
    'polygon': set(('onedge onpoint points skip scale distancebetween duration '
                    'matchcasterdirection yoffset').split()),
    'slash': set(('onpoint points width height angle duration matchcasterdirection yoffset').split()),
}
CALLBACKS = {'s', 'ontick', 'onhit', 'onend', 'onedge', 'onpoint'}
TARGETERS = {'self', 'selflocation', 'target', 'targetlocation', 'origin', 'playersinradius', 'playersnearorigin'}
PARTICLES = {'FLAME', 'SMOKE', 'CLOUD', 'END_ROD', 'CRIT', 'ELECTRIC_SPARK', 'DUST',
             'DUST_COLOR_TRANSITION', 'BLOCK'}
BOOLS = set(('fromorigin stopatentity stopatblock hitplayers hitnonplayers '
             'refreshduration cancelondeath canceloncasterdeath cancelonchangeworld '
             'matchcasterdirection').split())
POSITIVE = set(('distancebetween interval points ringpoints maxrange maxdistance velocity '
                'width height scale size ticks maxstacks').split())
NONNEGATIVE = set(('amount radius ringradius helixradius duration hs vs spread count').split())
INTEGER = {'amount', 'count', 'points', 'ringpoints', 'ticks', 'maxstacks', 'duration', 'interval'}
ID = re.compile(r'^[A-Za-z][A-Za-z0-9_-]*$')
DYNAMIC = re.compile(r'^<skill\.[a-zA-Z][a-zA-Z0-9_-]*>$')
NUMBER = re.compile(r'^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$')
COLOR = re.compile(r'^#[0-9a-fA-F]{6}$')


def parameters(text):
    """Parse the flat semicolon parameter lists actually used by the kit."""
    result = {}
    for item in text.split(';'):
        if not item or '=' not in item:
            raise ValueError(f'unsupported parameter syntax: {item!r}')
        key, value = item.split('=', 1)
        key, value = key.strip().lower(), value.strip()
        if not key or not value:
            raise ValueError('empty parameter key or value')
        if key in result:
            raise ValueError(f'duplicate mechanic parameter: {key}')
        result[key] = value
    return result


def balanced(text):
    stack = []
    for char in text:
        if char in '{[':
            stack.append(char)
        elif char in '}]':
            if not stack or stack.pop() != {'}': '{', ']': '['}[char]:
                return False
    return not stack


def parse_line(text):
    if not balanced(text):
        raise ValueError('unbalanced parameter groups')
    if text.startswith('delay '):
        if not re.fullmatch(r'delay [1-9]\d*', text):
            raise ValueError('unsupported delay; expected positive integer ticks')
        return 'delay', {}, ''
    match = re.fullmatch(r'([a-zA-Z][a-zA-Z0-9_]*)\{([^{}\[\]]+)\}(.*)', text)
    if not match:
        raise ValueError('unsupported mechanic line (checker accepts flat parameters only)')
    return match[1].lower(), parameters(match[2]), match[3].strip()


def validate(root: Path):
    root = root.resolve()
    errors, warnings, dynamic = [], [], []
    definitions, mobs, documents = {}, {}, []
    source_files = sorted(set(root.rglob('*.yml')) | set(root.rglob('*.yaml')))
    skill_lines, references = [], []
    graph = {}

    def error(where, message):
        errors.append(f'{where}: {message}')

    if not source_files:
        error(str(root), 'no YAML files found')
    for path in source_files:
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding='utf-8-sig')
            if '\t' in text:
                raise ValueError('tabs are not allowed in kit YAML')
            content = yaml.load(text, Loader=UniqueLoader)
            if not isinstance(content, dict) or not content:
                raise ValueError('expected a nonempty YAML mapping')
        except (yaml.YAMLError, ValueError) as exc:
            error(rel, str(exc))
            continue
        documents.append(rel)
        if path.name == 'packinfo.yml':
            if not all(k in content for k in ('Name', 'Version', 'Author', 'Description')):
                error(rel, 'packinfo missing required kit metadata')
            continue
        is_mob = 'mobs' in (p.lower() for p in path.relative_to(root).parts)
        table = mobs if is_mob else definitions
        for name, body in content.items():
            where = f'{rel}::{name}'
            if not isinstance(name, str) or not ID.fullmatch(name):
                error(where, 'invalid kit identifier')
                continue
            if name in table:
                error(where, f'duplicate definition; already in {table[name]}')
            table[name] = rel
            if not isinstance(body, dict):
                error(where, 'definition must be a mapping')
                continue
            if is_mob and not isinstance(body.get('Type'), str):
                error(where, 'mob needs Type')
            if is_mob and isinstance(body.get('Options'), dict) and body['Options'].get('NoAI') is True and body.get('Skills'):
                error(where, 'NoAI=true prevents skill casting per current Mob Options documentation')
            if not is_mob:
                for key in body:
                    if key not in {'Skills', 'Cooldown', 'Conditions', 'TargetConditions', 'TriggerConditions'}:
                        error(where, f'unsupported metaskill field: {key}')
            if 'Cooldown' in body and (isinstance(body['Cooldown'], bool) or not isinstance(body['Cooldown'], (int, float)) or body['Cooldown'] < 0):
                error(where, 'kit Cooldown must be nonnegative numeric seconds')
            for condition_key in ('Conditions', 'TargetConditions', 'TriggerConditions'):
                if condition_key not in body:
                    continue
                conditions = body[condition_key]
                if not isinstance(conditions, list) or any(not isinstance(x, str) for x in conditions):
                    error(where, f'{condition_key} must be a string list')
                else:
                    for cond in conditions:
                        if cond != 'offgcd' and not re.fullmatch(r'targetwithin\{d=\d+(?:\.\d+)?\} true', cond):
                            error(where, f'unsupported condition: {cond}')
            lines = body.get('Skills')
            if not isinstance(lines, list) or not lines:
                error(where, 'Skills must be a nonempty list')
                continue
            for index, line in enumerate(lines, 1):
                skill_lines.append((where, name, line, is_mob, index))

    for where, name, line, is_mob, index in skill_lines:
        loc = f'{where}.Skills[{index}]'
        if not isinstance(line, str):
            error(loc, 'skill line must be a string (quote YAML-sensitive values)')
            continue
        if not is_mob and '~on' in line:
            error(loc, 'triggers belong in mobs, not metaskills')
        try:
            head, attrs, tail = parse_line(line)
            if head == 'particleequation':
                raise ValueError('ParticleEquation is documented nonfunctional/WIP')
            if head == 'delay':
                continue
            if head not in ATTRS:
                raise ValueError(f'unsupported mechanic: {head}')
            unknown = attrs.keys() - ATTRS[head]
            if unknown:
                raise ValueError(f'unsupported {head} attributes: {sorted(unknown)}')
            for key, value in attrs.items():
                if '<' in value or '>' in value:
                    if not DYNAMIC.fullmatch(value) or not definitions.get(name, '').endswith('premium-parameters.skills.yml'):
                        raise ValueError('dynamic values only supported in the optional Premium template')
                    dynamic.append(f'{loc}: {key}={value} (not evaluated)')
                    continue
                if key in BOOLS and value.lower() not in {'true', 'false'}:
                    raise ValueError(f'{key} needs true/false')
                if key in POSITIVE | NONNEGATIVE:
                    if not NUMBER.fullmatch(value):
                        raise ValueError(f'{key} needs a number or supported parameter')
                    number = float(value)
                    if key in POSITIVE and number <= 0:
                        raise ValueError(f'{key} must be positive')
                    if key in NONNEGATIVE and number < 0:
                        raise ValueError(f'{key} must be nonnegative')
                    if key in INTEGER and not number.is_integer():
                        raise ValueError(f'{key} must be an integer in kit templates')
                if key in {'color', 'color2'} and not COLOR.fullmatch(value):
                    raise ValueError(f'{key} needs #RRGGBB')
                if key in CALLBACKS:
                    references.append((loc, value))
                    if head == 'skill' and not is_mob:
                        graph.setdefault(name, set()).add(value)

            if head.startswith('particle'):
                particle = attrs.get('particle', '').upper()
                if particle not in PARTICLES:
                    raise ValueError(f'unsupported or missing particle type: {particle!r}')
                required = {'DUST': {'color', 'size'}, 'DUST_COLOR_TRANSITION': {'color', 'color2', 'size'}, 'BLOCK': {'material'}}.get(particle, set())
                if required - attrs.keys():
                    raise ValueError(f'{particle} missing particle data: {sorted(required - attrs.keys())}')
                if particle not in {'DUST', 'DUST_COLOR_TRANSITION'} and {'color', 'color2', 'size'} & attrs.keys():
                    raise ValueError(f'kit does not support dust data for {particle}')
                if particle != 'BLOCK' and 'material' in attrs:
                    raise ValueError('kit material data requires BLOCK')
                if head in {'particlering', 'particleline', 'particlelinehelix', 'particlelinering'}:
                    if NUMBER.fullmatch(attrs.get('amount', '1')) and float(attrs.get('amount', '1')) > 4:
                        warnings.append(f'{loc}: unusually high per-sample count; review particle budget')

            if head == 'skill' and 's' not in attrs:
                raise ValueError('skill needs s callback')
            if head == 'skill' and attrs.get('s') == 'NXK_Premium_Burst' and not {'count', 'spread'} <= attrs.keys():
                raise ValueError('NXK_Premium_Burst requires count and spread')
            if tail:
                target = re.match(r'^@([a-zA-Z]+)(?:\{([^{}]+)\})?(?:\s+|$)', tail)
                if not target:
                    raise ValueError(f'unsupported target/trigger suffix: {tail}')
                target_name = target[1].lower()
                if target_name not in TARGETERS:
                    raise ValueError(f'unsupported targeter: {target[1]}')
                opts = parameters(target[2]) if target[2] else {}
                if target_name in {'playersinradius', 'playersnearorigin'}:
                    if set(opts) != {'r'} or not NUMBER.fullmatch(opts['r']) or float(opts['r']) <= 0:
                        raise ValueError('radius targeter requires positive r')
                elif opts:
                    raise ValueError('kit singleton targeter takes no parameters')
                if head == 'damage' and target_name in {'origin', 'selflocation', 'targetlocation'}:
                    raise ValueError('damage needs entity targets, not location targeter')
                suffix = tail[target.end():].strip()
                if suffix:
                    if not is_mob or not re.fullmatch(r'~on(?:Spawn|Interact|Timer:[1-9]\d*)', suffix):
                        raise ValueError(f'unsupported trigger: {suffix}')
                elif is_mob:
                    raise ValueError('kit mob lines require an explicit trigger')
            elif is_mob:
                raise ValueError('kit mob lines require targeter and explicit trigger')
        except ValueError as exc:
            error(loc, str(exc))

    for loc, destination in references:
        if destination not in definitions:
            error(loc, f'missing skill/callback: {destination}')
    visited, active = set(), set()

    def visit(node):
        if node in active:
            error(node, 'recursive synchronous skill calls are not supported by kit checker')
            return
        if node in visited:
            return
        active.add(node)
        for dest in graph.get(node, set()):
            visit(dest)
        active.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)
    return {
        'status': 'passed' if not errors else 'failed',
        'validation_kind': 'YAML parsing and static checks for the NXK subset',
        'runtime_tested': False,
        'server_profile_intent': 'MythicMobs 5.14.0; exact supported Paper/Minecraft build must be tested',
        'yaml_files': len(source_files), 'yaml_parsed': len(documents),
        'metaskills': len(definitions), 'mobs': len(mobs),
        'skill_lines': len(skill_lines), 'references_checked': len(references),
        'dynamic_values_not_evaluated': dynamic, 'warnings': warnings, 'errors': errors,
        'files': documents,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1] / 'assets' / 'templates')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = validate(args.root)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding='utf-8')
    print(rendered, end='')
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    sys.exit(main())
