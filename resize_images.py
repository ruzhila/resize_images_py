import os
from optparse import OptionParser
from PIL import Image
"""
Resize images to a specific size or percentage

requirements:
- Pillow (PIL fork)
```bash
python resize_images.py -i input.jpg -o output.jpg -s 100k
python resize_images.py -i input.jpg -o output.jpg -s 50%
python resize_images.py -i input_dir -o output_dir -s 100k
```
"""


def convert_file(input_file, output_file, max_size, percent, format):
    """convert input file to output file with max_size or percent
    """
    if os.path.isdir(output_file):
        output_file = os.path.join(
            output_file, os.path.basename(input_file))

    if os.path.exists(output_file):
        print(f'{output_file} exists, skipping')
        return

    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with Image.open(input_file) as img:
        img_size = os.path.getsize(input_file)
        if percent:
            width, height = img.size
            max_width = int(width * max_size)
            max_height = int(height * max_size)
            img = img.resize((max_width, max_height), Image.LANCZOS)
        else:
            # check file size
            if img_size < max_size:
                print(f'{input_file} ({img_size}) -> {output_file} (skip)')
                return

            # calculate new size
            width, height = img.size
            scale_factor = (max_size / img_size) ** 0.59
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            img = img.resize((new_width, new_height), Image.LANCZOS)
        try:
            img.save(output_file, format=format)
            new_size = os.path.getsize(output_file)
            print(f'{input_file} ({img_size}) -> {output_file} ({new_size})')
        except OSError as e:
            print(f'{input_file} failed: ({e})')


def walk_dir(input_dir, output_dir, max_size, percent, format):
    """walk through input_dir and convert images to output_dir
    """
    for root, _, files in os.walk(input_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in ('.jpg', '.jpeg', '.png'):
                continue
            input_file = os.path.join(root, file)
            output_file = input_file.replace(input_dir, output_dir)
            convert_file(input_file, output_file,
                         max_size, percent, format)


def main():
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      default=".", help="Input image file", metavar="INPUT")
    parser.add_option("-o", "--output", dest="output",
                      default=".", help="Output image file", metavar="OUTPUT")
    parser.add_option("-s", "--size", dest="size", default="80%",
                      help="Output image size", metavar="SIZE")
    parser.add_option("-f", "--format", dest="format",
                      default="jpeg", help="Output image format", metavar="FORMAT")

    (options, _) = parser.parse_args()
    max_size = options.size.lower()
    percent = False

    if max_size.endswith('%'):
        max_size = int(max_size[:-1])
        if max_size < 1 or max_size > 100:
            parser.error('Invalid percentage')
        max_size = max_size / 100.0
        percent = True
    else:
        unit = max_size[-1]
        units = {'k': 1024, 'm': 1024**2, 'g': 1024**3}
        if unit in units:
            max_size = int(max_size[:-1])
            max_size *= units[unit]
        else:
            parser.error('Invalid size format')

    # check if input file exists
    if os.path.isfile(options.input):
        convert_file(options.input, options.output,
                     max_size, percent, options.format)
    elif os.path.isdir(options.input):
        walk_dir(options.input, options.output,
                 max_size, percent, options.format)
    else:
        parser.error(f'{options.input} does not exist')


if __name__ == '__main__':
    main()
