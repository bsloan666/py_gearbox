import argparse
import assembly as assem

def parse_command_line():
    """
    Standard argparse stuff
    """
    parser = argparse.ArgumentParser(
        prog="gearbox",
        description="A tool for generating 3D-printable gearboxes",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="Choose a single subcommand"
    )

    subparsers = parser.add_subparsers(dest='operation')

    gear_parser = subparsers.add_parser(
        "gear", 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Generate a single spur gear"
    )
    reducer_parser = subparsers.add_parser(
        "reducer", 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="generate gearbox consisting of a stack of reduction gears"
    )
    planetary_parser = subparsers.add_parser(
        "planetary", 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="generate a planetary gearbox"
    )
    bevel_parser = subparsers.add_parser(
        "bevel", 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="generate a right angle gearbox"
    )
    cycloid_parser = subparsers.add_parser(
        "cycloid", 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="generate a cycloidal hub and ring"
    )

    cycloid_parser.add_argument(
        "--waves",
        type=int,
        default=10,
        dest="waves",
        help="The number of sinusoidal 'teeth' in the eccentric hub",
    )

    cycloid_parser.add_argument(
        "--crest",
        type=float,
        default=2,
        dest="crest",
        help="The amplitude of the sinusoidal 'teeth' in mm",
    )

    cycloid_parser.add_argument(
        "--travel",
        type=float,
        default=2,
        dest="travel",
        help="The eccentricity of the cog in mm from center",
    )

    planetary_parser.add_argument(
        "--sun-radius",
        type=float,
        default=7,
        dest="sun_radius",
        help="amount of speed reduction in a single stage",
    )

    planetary_parser.add_argument(
        "--ring-radius",
        type=float,
        default=35.7,
        dest="ring_radius",
        help="total number of stages",
    )

    planetary_parser.add_argument(
        "--planet-axle-radius",
        type=float,
        default=11.15,
        dest="planet_axle_radius",
        help="radius of inner axle",
    )

    planetary_parser.add_argument(
        "--sun-axle-radius",
        type=float,
        default=2.6,
        dest="sun_axle_radius",
        help="radius of inner axle",
    )

    reducer_parser.add_argument(
        "--step-ratio",
        type=float,
        default=0.333333,
        dest="step_ratio",
        help="amount of speed reduction in a single stage",
    )

    reducer_parser.add_argument(
        "--repeats",
        type=int,
        default=4,
        dest="repeats",
        help="total number of stages",
    )

    reducer_parser.add_argument(
        "--minor-radius",
        type=float,
        default=12,
        dest="minor_radius",
        help="radius of smallest cog",
    )

    reducer_parser.add_argument(
        "--flip",
        type=int,
        default=0,
        dest="flip",
        help="put small cog on top (1) vs. bottom (0)",
    )

    parser.add_argument(
        "--axle-radius",
        type=float,
        default=2.6,
        dest="axle_radius",
        help="radius of inner axle",
    )

    parser.add_argument(
        "--second-axle-radius",
        type=float,
        default=11,
        dest="second_axle_radius",
        help="radius of alternate axle",
    )

    parser.add_argument(
        "--radius",
        type=float,
        default=16,
        dest="radius",
        help="radius of single cog",
    )

    parser.add_argument(
        "--twist",
        type=float,
        default=150.0,
        dest="twist",
        help="twist in degrees for helical gears",
    )

    parser.add_argument(
        "--depth",
        type=float,
        default=6,
        dest="depth",
        help="thickness of single cog",
    )

    parser.add_argument(
        "--pitch",
        type=float,
        default=3,
        dest="pitch",
        help="the size of a tooth in mm",
    )


    parser.add_argument(
        "--directory",
        type=str,
        default="/var/tmp/assembly",
        dest="out_dir",
        help="output_directory",
    )

    args = parser.parse_args()
    return args


def run():
    args = parse_command_line()

    if args.operation == "planetary":
        assem.planetary(
            args.sun_radius, 
            args.ring_radius, 
            args.planet_axle_radius, 
            args.sun_axle_radius, 
            args.depth, 
            args.pitch,
            args.twist, 
            args.out_dir
        )

    elif args.operation == "cycloid":
        assem.cycloidal_drive(
            args.radius, 
            7.5, 
            2.6, 
            args.travel, 
            args.depth, 
            args.waves, 
            args.crest, 
            args.out_dir
        )
    elif args.operation == "reducer":    
        assem.reducer_stack(
            args.step_ratio, 
            args.repeats, 
            args.minor_radius, 
            args.axle_radius, 
            args.depth, 
            args.flip,
            args.pitch,
            args.twist, 
            args.out_dir,
        )
        
        total_speed_reduction = args.step_ratio ** args.repeats
        print("Total speed reduction is {0}".format(total_speed_reduction))

    elif args.operation == "bevel":    
        assem.right_angle_transmission(
            args.radius,
            args.axle_radius,
            args.second_axle_radius,
            args.depth, 
            args.twist, 
            args.out_dir
        )
    elif args.operation == "gear":
        assem.single_gear(
            args.radius, 
            args.axle_radius,
            args.pitch,
            args.depth,
            args.out_dir
        )

if __name__ == "__main__":
    run()
