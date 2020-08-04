#!/usr/bin/env python3

import sys
import xmltodict
import dicttoxml
import xml

if len(sys.argv) != 4:
    print('usage: ./avorion-gridify <grid-size> <original_ship.xml> <modified_ship.xml>')
    print('example: ./avorion-gridify 0.5 myships/ship.xml experiments/newship.xml')
    sys.exit(1)

grid = float(sys.argv[1])

with open(sys.argv[2], "r") as handle:
    xmltext = handle.read()

ship = xmltodict.parse(xmltext)

xmltext = '<?xml version="1.0" encoding="utf-8"?>\n'

# write to XML and snap values to grid
for ship_design in ship:
    if not ship_design.startswith('ship_design'):
        raise Exception('unsupported XML block: ' + ship_design)

    design = ship[ship_design]
    plan = design['plan']

    xmltext += '<' + ship_design + '>\n'
    xmltext += '\t<plan accumulateHealth="{}" convex="{}">\n'.format(plan['@accumulateHealth'], plan['@convex'])

    for item in plan['item']:
        xmltext += '\t\t<item parent="{}" index="{}">\n'.format(item['@parent'], item['@index'])

        upscale = 1.0 / grid
        downscale = grid

        block = item['block']
        # snap values instead of simply dumping them again
        lx = str(round(float(block['@lx']) * upscale) * downscale)
        ly = str(round(float(block['@ly']) * upscale) * downscale)
        lz = str(round(float(block['@lz']) * upscale) * downscale)
        ux = str(round(float(block['@ux']) * upscale) * downscale)
        uy = str(round(float(block['@uy']) * upscale) * downscale)
        uz = str(round(float(block['@uz']) * upscale) * downscale)
        index = block['@index']
        material = block['@material']
        look = block['@look']
        up = block['@up']
        color = block['@color']
        xmltext += '\t\t\t<block lx="{}" ly="{}" lz="{}" ux="{}" uy="{}" uz="{}" index="{}" material="{}" look="{}" up="{}" color="{}"/>\n'.format(
                lx, ly, lz, ux, uy, uz, index, material, look, up, color)

        xmltext += '\t\t</item>\n'
    # end for

    xmltext += '\t</plan>\n'
    xmltext += '</' + ship_design + '>\n'

with open(sys.argv[3], "w") as handle:
    handle.write(xmltext)
