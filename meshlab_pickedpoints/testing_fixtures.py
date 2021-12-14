EXAMPLE_PICKED_POINTS_XML_STRING = """
<!DOCTYPE PickedPoints>
<PickedPoints>
 <DocumentData>
  <DateTime time="16:00:00" date="2014-12-31"/>
  <User name="bodylabs"/>
  <DataFileName name="ignored.obj"/>
 </DocumentData>
 <point x="0.044259" y="0.467733" z="-0.060032" name="Femoral_epicon_med_lft"/>
<point x="0.017893" y="1.335375" z="0.01839" name="Clavicale_lft"/>
<point x="0.000625" y="1.124424" z="0.08093" name="Substernale"/>
</PickedPoints>
"""

EXAMPLE_POINTS = [
    {
        "name": "Femoral_epicon_med_lft",
        "point": [0.044259, 0.467733, -0.060032],
    },
    {"name": "Clavicale_lft", "point": [0.017893, 1.335375, 0.018390]},
    {"name": "Substernale", "point": [0.000625, 1.124424, 0.080930]},
]