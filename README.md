# A tool for batch resizing images to smaller dimensions using Python

This tool can be used to resize images in batches, specify the input and output directories, and save all images in the input directory to the output directory after resizing. It also supports specifying the format of the conversion:

By [ruzhila.cn](http://ruzhila.cn/?from=github_resize_images_py).

### 🚀 [100-line-code](https://github.com/ruzhila/100-line-code)  A collection of learning projects written in 100 lines of code

## Features

- **Parse command line parameters:** Especially the `-s` parameter, which supports formats such as `100k` and `80%`. When parsing parameters, determine whether the size is fixed or a percentage, and execute different logic based on the parameters.
- **Traverse files:** Use `os.walk` to traverse all files in the folder, and only process images such as `.jpeg/.jpeg/.png`.
- **Adjust image size:** Use the Pillow library to adjust the image size. If the `-f/--format` format is not specified, keep the original format.

## Usage

```bash
pip install -r requirements.txt
python resize_images.py -i . -o /tmp/ -s 100k -f jpg
python resize_images.py -i input.jpg -o output.jpg -s 100k
python resize_images.py -i input.jpg -o output.jpg -s 50%
python resize_images.py -i input_dir -o output_dir -s 100k
```
