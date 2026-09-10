import getopt
from generator import Generator, CHARACTERS_FILE, WORDS_FILE
from exceptions import GenException
import os
import sys

PROGRAM_NAME = 'cli.py';

def usage():
    print('usage: ' + PROGRAM_NAME + '\n' + \
            ' <default>\n' + \
            '   --characters=<chinese characters>\n' + \
            '   [--title=<custom title>]\n' + \
            '   [--guide=star]\n' + \
            '   [--stroke-order-color=black]\n' + \
            '   [--character-guide-opacity=100]\n' + \
            '   [--stroke-order-opacity=100]\n' + \
            ' --info\n' + \
            '   --characters=<chinese characters>\n' + \
            ' --sheet\n' + \
            '   [--title=<custom title>]\n' + \
            '   [--guide=star]\n' + \
            '   [--stroke-order-color=black]\n' + \
            '   [--character-guide-opacity=100]\n' + \
            '   [--stroke-order-opacity=100]');

def parse_opacity(value, opt_name):
    try:
        val = int(value)
        if val < 0 or val > 100:
            print('Error: ' + opt_name + ' must be an integer between 0 and 100')
            sys.exit(1)
        return val
    except ValueError:
        print('Error: ' + opt_name + ' must be an integer between 0 and 100')
        sys.exit(1)

def main(argv):
    characters = '';
    title = '';
    guide = '';
    stroke_order_color = '';
    character_guide_opacity = None;
    stroke_order_opacity = None;
    info_mode = False;
    sheet_mode = False;
    opts, args = getopt.getopt(argv, '', \
            ['characters=', 'title=', 'guide=', \
            'stroke-order-color=', 'character-guide-opacity=', \
            'stroke-order-opacity=', 'info', 'sheet']);
    for opt, arg in opts:
        if opt == '--characters':
            characters = arg;
        elif opt == '--title':
            title = arg;
        elif opt == '--guide':
            guide = arg;
        elif opt == '--stroke-order-color':
            stroke_order_color = arg;
        elif opt == '--character-guide-opacity':
            character_guide_opacity = parse_opacity(arg, '--character-guide-opacity');
        elif opt == '--stroke-order-opacity':
            stroke_order_opacity = parse_opacity(arg, '--stroke-order-opacity');
        elif opt == '--info':
            info_mode = True;
        elif opt == '--sheet':
            sheet_mode = True;
        else:
            usage();
            exit(1);

    if 'MAKEMEAHANZI' in os.environ:
        makemeahanzi = os.environ['MAKEMEAHANZI'];
    else:
        raise GenException('MAKEMEAHANZI enviroment variable not set');

    if 'CEDICT' in os.environ:
        cedict = os.environ['CEDICT'];
    else:
        raise GenException('CEDICT enviroment variable not set');

    if info_mode == sheet_mode:
        info_mode = True;
        sheet_mode = True;

    if (info_mode and characters == '') \
            or (sheet_mode and not info_mode and characters != '') \
            or (info_mode and not sheet_mode and title != ''):
        usage();
        exit(1);

    working_dir = os.getcwd();
    try:
        g = Generator(makemeahanzi);
        guide_val = g.get_guide(guide);
        if info_mode == sheet_mode:
            g.generate_infos(makemeahanzi, cedict, working_dir, characters);
            g.generate_sheet(makemeahanzi, working_dir, title, guide_val, stroke_order_color, character_guide_opacity=character_guide_opacity, stroke_order_opacity=stroke_order_opacity);
            g.delete_files(working_dir, CHARACTERS_FILE.replace('.', '\.'));
            g.delete_files(working_dir, WORDS_FILE.replace('.', '\.'));
        elif info_mode:
            g.generate_infos(makemeahanzi, cedict, working_dir, characters);
        else:
            g.generate_sheet(makemeahanzi, working_dir, title, guide_val, stroke_order_color, character_guide_opacity=character_guide_opacity, stroke_order_opacity=stroke_order_opacity);
    except GenException as e:
        print(str(e));

if __name__ == '__main__':
    main(sys.argv[1:]);
