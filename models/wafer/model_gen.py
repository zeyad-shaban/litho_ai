#!/usr/bin/env python3
"""
Generate wafer SDF with a grid of crosses.
Usage: python3 generate_wafer_sdf.py [--output <path>]
"""

import argparse

def generate_wafer_sdf(output_file):
    # Realistic parameters (all in meters, kg)
    wafer_radius = 50e-3            # 50 mm
    wafer_thickness = 0.5e-3       # 0.5 mm
    wafer_mass = 0.01              # 10 g

    # Marker dimensions (realistic)
    marker_arm_length = 200e-6     # 200 µm
    marker_arm_width = marker_arm_length / 4     # 50 µm
    marker_height = 10e-6       # 1 µm
    marker_z = (wafer_thickness / 2.0) + (marker_height / 2.0)  # 0.0002505 m

    # Grid: 5x5, 10 mm spacing, fits entirely inside wafer
    grid_spacing = 0.01            # 10 mm
    grid_points = 5                # 5x5
    half_range = (grid_points - 1) * grid_spacing / 2.0  # 0.02 m
    grid_min = -half_range         # -0.02 m
    grid_max = half_range          # 0.02 m

    # Inertia for a thin cylinder
    ixx = (1.0/12.0) * wafer_mass * (3*wafer_radius**2 + wafer_thickness**2)
    iyy = ixx
    izz = 0.5 * wafer_mass * wafer_radius**2

    lines = [
        '<?xml version="1.0"?>',
        '<sdf version="1.9">',
        '  <model name="wafer_grid">',
        '    <link name="link">',
        '',
        '      <visual name="wafer_visual">',
        '        <geometry>',
        '          <cylinder>',
        f'            <radius>{wafer_radius}</radius>',
        f'            <length>{wafer_thickness}</length>',
        '          </cylinder>',
        '        </geometry>',
        '        <material>',
        '          <ambient>0.6 0.6 0.7 1</ambient>',
        '          <diffuse>0.6 0.6 0.7 1</diffuse>',
        '          <specular>0.2 0.2 0.2 1</specular>',
        '        </material>',
        '      </visual>',
        '',
        '      <collision name="collision">',
        '        <geometry>',
        '          <cylinder>',
        f'            <radius>{wafer_radius}</radius>',
        f'            <length>{wafer_thickness}</length>',
        '          </cylinder>',
        '        </geometry>',
        '      </collision>',
        '',
        '      <inertial>',
        f'        <mass>{wafer_mass}</mass>',
        '        <inertia>',
        f'          <ixx>{ixx}</ixx>',
        f'          <iyy>{iyy}</iyy>',
        f'          <izz>{izz}</izz>',
        '          <ixy>0</ixy>',
        '          <ixz>0</ixz>',
        '          <iyz>0</iyz>',
        '        </inertia>',
        '      </inertial>',
        ''
    ]

    # Generate crosses for each grid point
    for i in range(grid_points):
        x = grid_min + i * grid_spacing
        for j in range(grid_points):
            y = grid_min + j * grid_spacing
            # Horizontal bar
            lines.append(f'      <visual name="cross_h_{x}_{y}">')
            lines.append(f'        <pose>{x} {y} {marker_z} 0 0 0</pose>')
            lines.append('        <geometry>')
            lines.append('          <box>')
            lines.append(f'            <size>{marker_arm_length} {marker_arm_width} {marker_height}</size>')
            lines.append('          </box>')
            lines.append('        </geometry>')
            lines.append('        <material>')
            lines.append('          <ambient>0 0 0 1</ambient>')
            lines.append('          <diffuse>0 0 0 1</diffuse>')
            lines.append('        </material>')
            lines.append('      </visual>')
            # Vertical bar
            lines.append(f'      <visual name="cross_v_{x}_{y}">')
            lines.append(f'        <pose>{x} {y} {marker_z} 0 0 0</pose>')
            lines.append('        <geometry>')
            lines.append('          <box>')
            lines.append(f'            <size>{marker_arm_width} {marker_arm_length} {marker_height}</size>')
            lines.append('          </box>')
            lines.append('        </geometry>')
            lines.append('        <material>')
            lines.append('          <ambient>0 0 0 1</ambient>')
            lines.append('          <diffuse>0 0 0 1</diffuse>')
            lines.append('        </material>')
            lines.append('      </visual>')

    lines.append('    </link>')
    lines.append('  </model>')
    lines.append('</sdf>')

    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Wafer SDF generated at {output_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='/home/zeyadcode/litho_ai/models/wafer/model.sdf',
                        help='Output SDF file path')
    args = parser.parse_args()
    generate_wafer_sdf(args.output)

if __name__ == '__main__':
    main()