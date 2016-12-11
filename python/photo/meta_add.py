import sys
import getopt
import exifread
from pathlib import Path, PurePath
import shutil


#TODO:
# - handle files with '.' in names
# - add support for basename parameter

# extract EXIF metadata from file
def get_meta_info(file_path):
    # Open image file for reading (binary mode)
    f = open(file_path, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f)

    return tags


# create new filename using exif metainf
def create_new_name(filepath, dst_path):
    exif_tags = get_meta_info(str(filepath))

    if 'EXIF DateTimeOriginal' in exif_tags.keys():
        #exif_datetime_original = str(exif_tags['EXIF DateTimeOriginal']).replace(':', '.').replace(' ', '_')[:-3]
        exif_datetime_original = str(exif_tags['EXIF DateTimeOriginal']).replace(':', '.')[:-3]

        (file_name, ext) = filepath.name.split('.')
        new_path = PurePath(dst_path).joinpath(exif_datetime_original + ' - ' + file_name + '.' + ext)

        return new_path
    else:
        print("Error processing {} file. No suitable EXIF tags found".format(filepath))


# rename file
def rename(src, dst):
    shutil.copy(str(src), str(dst))


# gel list of files in specified folder
def find_files(basepath):

    data_path = Path(basepath)
    for file in data_path.iterdir():
        if file.is_file():
            yield file


# parse command line arguments
def parse_cmd_args(argv):

    input_path = '.'
    output_path = '.'
    base_name = ''

    try:
        opts, args = getopt.getopt(argv,"hi:o:b:",["ipath=","opath=","basen="])
    except getopt.GetoptError:
        print ('meta_add.py -i <inputpath> -o <outputpath> -b <basename>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('meta_add.py -i <inputpath> -o <outputpath> -b <basename>')
            sys.exit()
        elif opt in ("-i", "--ipath"):
            input_path = arg
        elif opt in ("-o", "--opath"):
            output_path = arg
        elif opt in ["-b", "--basen"]:
            base_name = arg

    return (input_path, output_path, base_name)


if __name__ == "__main__":
    (input_path, output_path, base_name) = parse_cmd_args(sys.argv[1:])

    for filepath in find_files(input_path):
        rename(filepath, create_new_name(filepath, output_path))