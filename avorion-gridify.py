#!/usr/bin/env python3

import xmltodict
import dicttoxml
import xml
import argparse
import sys

if __name__ == "__main__":

    HELP_TEXT = 'Round sizes of your ship to integer multiples of grid size'
    parser = argparse.ArgumentParser(description=HELP_TEXT)

    parser.add_argument("GRID_SIZE",   type=float, help="Grid size to align to")
    parser.add_argument("ORIG_FILE",   type=str,   help="XML-file describing your ship")
    parser.add_argument("TARGET_FILE", type=str,   help="XML-file to save the ship to")
    args = parser.parse_args()

    grid = args.GRID_SIZE
    
    with open(args.ORIG_FILE, "r") as handle:
        xmltext = handle.read()

    ship = None
    try:
        ship = xmltodict.parse(xmltext)
    except xml.parsers.expat.ExpatError as e:
        print("Invalid XML: {}".format(e))
        sys.exit(1)
    
    xmltext = '<?xml version="1.0" encoding="utf-8"?>\n'
    
    # write to XML and snap values to grid
    for ship_design in ship:
        if not ship_design.startswith('ship_design'):
            raise Exception('unsupported XML block: ' + ship_design)
    
        design = ship[ship_design]
        plan = design['plan']
    
        xmltext += '<' + ship_design + '>\n'
        helperText = '\t<plan accumulateHealth="{}" convex="{}">\n'
        xmltext += helperText.format(plan['@accumulateHealth'], plan['@convex'])
    
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
            line =  '\t\t\t<block lx="{}" ly="{}" lz="{}" ux="{}" uy="{}" uz="{}"'
            line += 'index="{}" material="{}" look="{}" up="{}" color="{}"/>\n'
            xmltext += line.format(lx, ly, lz, ux, uy, uz, index, material, look, up, color)
    
            xmltext += '\t\t</item>\n'
        # end for
    
        xmltext += '\t</plan>\n'
        xmltext += '</' + ship_design + '>\n'
    
    with open(args.TARGET_FILE, "w") as handle:
        handle.write(xmltext)
