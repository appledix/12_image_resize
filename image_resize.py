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
    return parser.parse_args()

def get_proportions(image_size):
    return image_size[0] / image_size[1]

def are_proportions_fine(first_image_size, second_image_size):
    original_proportions = get_proportions(first_image_size)
    new_proportions = get_proportions(second_image_size)
    return original_proportions == new_proportions

def is_user_wish_to_continue_with_broken_proportions():
    while True:
        user_answer = input("Warning!\nOriginal image proportions are different" \
            " from the input values. \nContinue?(Y,n):")
        if user_answer.lower() == "n": 
            return False
        elif user_answer.lower() in ["" ,"y"]:
            return True
        else:
            continue

def resize_image(image, width=None, height=None):
    if not width and not height:
        return image
    if not width or not height:
        proportions = get_proportions(image.size)
        width, height = (height * proportions, height) if (not width) \
        else (width, width / proportions)
    new_size = (int(width), int(height))
    return image.resize(new_size)

def get_output_image_name(new_image, original_image_name):
    width, height = new_image.size
    name_postfix = "__{}x{}".format(width, height)
    return original_image_name.replace('.', '{}.'.format(name_postfix))

def save_image(image, image_name, output_location):
    image.save(output_location + image_name)

def scale_sizes(image_size, scale): 
    return tuple(int(value*scale) for value in image_size)


def main():
    args = get_args_from_terminal()
    path_to_original_image, width, height, scale, output_location = \
    args.path_to_image, args.width, args.height, args.scale, args.output

    if scale and (width or height):
        print("You can't resize image with --scale and --width and/or --height" \
            " parameters simultaneously. Pick one method, not both.")
        return

    if output_location:
        if not os.path.isdir(output_location):
            print("Invalid output location.")
            return
        output_location += "/"
    else:
        print("The output location is not specified.\nResult image will be put into original image folder.")
        output_location = os.path.dirname(path_to_original_image)

    try:
        original_image = Image.open(path_to_original_image)
    except OSError as msg:
        print("Can't open original image.\nError: {}".format(msg))
        return

    if scale:
        width, height = scale_sizes(original_image.size, scale)
    elif width and height:
        if not are_proportions_fine(original_image.size, (width, height)):
            if not is_user_wish_to_continue_with_broken_proportions():
                return

    new_image = resize_image(original_image, width, height)
    original_image_name = os.path.basename(path_to_original_image)
    new_image_name = get_output_image_name(new_image, original_image_name)
    save_image(new_image, new_image_name, output_location)


if __name__ == '__main__':
    main()