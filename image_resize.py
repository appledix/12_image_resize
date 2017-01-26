import argparse
import os

from PIL import Image


def get_args_from_terminal():
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_image", help="Path to original image", type=str)
    parser.add_argument("-wt", "--width", help="Result image width", type=int)
    parser.add_argument("-ht", "--height", help="Result image height", type=int)
    parser.add_argument("-s", "--scale", help="Increase image N times", type=float)
    parser.add_argument("-o", "--output", help="Result image location", type=str)
    args = parser.parse_args()
    if not args.output:
        args.output = os.path.dirname(args.path_to_image)
    elif (not args.output.endswith('/')):
        args.output += "/"
    return args

def get_proportions(image_size):
    return image_size[0] / image_size[1]

def are_proportions_fine(first_image_size, second_image_size):
    return get_proportions(first_image_size) == get_proportions(second_image_size)

def resize_image(image, width=None, height=None, scale=None):
    if (not width) and (not height) and (not scale):
        return image
    else:
        if scale:
            width, height = scale_sizes(image.size, scale)
        elif (not width) or (not height):
            proportions = get_proportions(image.size)
            if not width:
                width = height * proportions
            else:
                height = width / proportions
        new_size = (int(width), int(height))
        return image.resize(new_size)

def get_output_image_name(new_image, path_to_original_image):
    original_image_name = os.path.basename(path_to_original_image)
    width, height = new_image.size
    name_postfix = "__{}x{}".format(width, height)
    return original_image_name.replace('.', '{}.'.format(name_postfix))

def save_image(image, image_name, output_location):
    image.save(output_location + image_name)

def scale_sizes(image_size, scale): 
    return tuple(int(value*scale) for value in image_size)

def main():
    args = get_args_from_terminal()
    if args.scale and (args.width or args.height):
        exit("You can't resize image with --scale and --width and/or --height"
             " parameters simultaneously. Pick one method, not both.")
    elif args.output and (not os.path.isdir(args.output)):
        exit("Invalid output location.")
    path_to_original_image, width, height, scale, output_location = \
    args.path_to_image, args.width, args.height, args.scale, args.output
    try:
        original_image = Image.open(path_to_original_image)
    except OSError as msg:
        exit("Can't open original image.\nError: {}".format(msg))
    if (width and height) \
    and (not are_proportions_fine(original_image.size, (width, height))):
        print("Warning!\nOriginal image proportions are different"
              " from the input values.")
    new_image = resize_image(original_image, width, height, scale)
    new_image_name = get_output_image_name(new_image, path_to_original_image)
    save_image(new_image, new_image_name, output_location)


if __name__ == '__main__':
    main()