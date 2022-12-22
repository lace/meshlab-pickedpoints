# Changelog

# 4.1.0

BREAKING CHANGES:

- Downgrade flake8 dependency
- Support Python 3.7


# 4.0.0

BREAKING CHANGES:

- Remove `__version__` property.
- Require Python 3.8.1 or later.


# 3.0.0

BREAKING CHANGES:

- Adopt Metabolize/Curvewise named points JSON schema.
- Remove NumPy dependency; return lists instead.

Old:

```py
{
  "Femoral_epicon_med_lft": np.array([0.044259, 0.467733, -0.060032]),
  "Clavicale_lft": np.array([0.017893, 1.335375, 0.018390]),
  "Substernale": np.array([0.000625, 1.124424, 0.080930]),
}
```

New:
```py
[
  {"name": "Femoral_epicon_med_lft", "point": [0.044259, 0.467733, -0.060032]},
  {"name": "Clavicale_lft", "point": [0.017893, 1.335375, 0.018390]},
  {"name": "Substernale", "point": [0.000625, 1.124424, 0.080930]},
]
```

New features:

- Add picked points to JSON conversion script: `python -m meshlab_pickedpoints.cli`.


# 2.0.0

Upgrade vg dependency.


# 1.0.0

Version bump. No changes.


# 1.0.0b0

Initial release.
