#####################
##   POST PROCESS  ##
#####################
from copy import deepcopy
from typing import Text, List, Dict, Any, Tuple
from PIL import Image, ImageFont, ImageDraw
from pylette.color_extraction import get_bg_fg_color
from translate_to_modern_vietnamese.translate_to_modern_vietnamese import translate_to_modern_vietnamese
from log.logger import setup_logger
import logging
setup_logger()

def postprocess_text(text: Text):
    # Uppercase characters
    text = text.upper()
    return text

# SRC: https://gist.github.com/Ze1598/420c7eb600899c86d1d65e83c3cc8b25
def get_text_dimensions(
    text_string: str,
    font: ImageFont
    ):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

def check_text_size(
    text_string: Text,
    direction: Text,
    width: int,
    height: int,
    font_path: Text = 'font/arial.ttf'
)->  Tuple:
    font_size = 1
    while True:
        pil_font = ImageFont.truetype(font_path, font_size)
        text_size = get_text_dimensions(
                text_string= text_string,
                font= pil_font
            )
        
        width_x = (width - text_size[0]) // 2
        height_y = (height - text_size[1]) // 2

        if (width_x < 0 or height_y < 0) and direction == 'horizontal':
            # Return font size before
            pil_font = ImageFont.truetype(font_path, font_size - 1)
            text_size = get_text_dimensions(
                    text_string= text_string,
                    font= pil_font
                )
            return text_size, pil_font, font_size
        else:
            font_size+=1

def rotate_vertical_bbox_rectange(
    bbox
):
    tl = bbox[0]
    br = bbox[1]
    x1, y1 = tl
    x2, y2 = br
    cen_x  =x1 + (x2 - x1) //2
    cen_y = y1 + (y2 - y1) //2
    print(cen_x, cen_y)

    #
    width = (x2 -x1)
    height = (y2 -y1)
    half_width = width // 2
    half_height = height // 2

    print(f'Half width: {half_width}, half height: {half_height}')


    # top-left corner
    x_tl = cen_x -half_height
    y_tl = cen_y -half_width
    print(f'tl: {(x_tl, y_tl)}')
    # rotate bottom right
    x_br = cen_x + half_height
    y_br = cen_y + half_width
    print(f'br: {(x_br, y_br)}')
    return ((x_tl, y_tl),(x_br, y_br))

def check_bbox_is_horizontal_rectangle(
    bbox
)-> bool:
    # region 1: Get top-left and bottom-right
    tl = bbox[0]
    br = bbox[1]
    # endregion

    # region 2: Get height and width
    x1, y1 = tl
    x2, y2 = br

    height = x2 - x1
    width = y2 - y1
    # endregion


    # region check bbox is horizontal rectangle
    if height > width: # vertical
        # region rotate rectangle I(tl[0],tl[1]) 
        return rotate_vertical_bbox_rectange(
            bbox=(tl, br)
        ), (height, width)
        # endregion
    # endregion
    return bbox, (height, width)

def draw_text_horizontal(
    text: str,
    direction: str,
    bbox: Tuple,
    draw: ImageDraw,
    fg_color: str
):
    tl = bbox[0]
    br = bbox[1]
    x1, y1 = tl
    x2, y2 = br

    width = (x2 -x1)
    height = (y2 -y1)
    # region Calculate Text Size
    text_size, pil_font, _ = check_text_size(
        text_string= text,
        direction = direction,
        width= width,
        height= height
    )
    # endregion
    # region get position
    width_x = (width - text_size[0]) // 2
    height_y = (height - text_size[1]) // 2
    x_pos = x1 + width_x
    y_pos = y1 + height_y
    position = (x_pos, y_pos)
    # endregion

    # region draw text
    draw.text(
        position,
        text,
        font=pil_font,
        fill=fg_color
    )
    # endregion


def draw_text_vertical(
    text: str,
    bbox: Tuple,
    draw: ImageDraw,
    fg_color: str,
    font_size: int,
    font_path : str = 'font/arial.ttf'
):
    tl = bbox[0]
    br = bbox[1]
    x1, y1 = tl
    x2, y2 = br
    width = (x2 -x1)
    height = (y2 -y1)
    # region get text size
    pil_font = ImageFont.truetype(font_path, font_size)
    text_size = get_text_dimensions(
                text_string= text,
                font= pil_font
            )
    # endregion

    # region get position
    width_x = (width - text_size[0]) // 2
    height_y = (height - text_size[1]) // 2
    x_pos = x1 + width_x
    y_pos = y1 + height_y
    position = (x_pos, y_pos)
    # endregion

    # region draw text
    draw.text(
        position,
        text,
        font=pil_font,
        fill=fg_color
    )
    # endregion

def _postprocess(
    image_fn: Text,
    list_dict_result: List[Dict[Text, Any]]
):
    # region Create a PIL image and draw each text using the custom font
    if isinstance(image_fn, str):
        pil_image = Image.open(image_fn)
    else:
        pil_image = Image.fromarray(image_fn)
    draw = ImageDraw.Draw(pil_image)
    # endregion


    for _dict in list_dict_result:
        # region extract input
        bbox, text= _dict['bbox'], _dict['text']
        if not text:
            continue
        logging.info(f"Text: {text}")
        # endregion

        # region 1. Unpack the bounding box
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))
        # endregion
        

        # region 2. Get image from bbox
        x1, y1 = tl
        x2,y2 = br
        cropped_image = pil_image.crop((x1, y1, x2, y2))
        # cropped_polygon_img = pil_image.
        # width_image = x2 - x1
        # height_image = y2 - y1
        # endregion

        # region 3. Get backgroud and foregroud color
        fg_color, bg_color = get_bg_fg_color(cropped_image)
        # endregion

        # region 4. Check image is horizontally or vertically
        if cropped_image.width >= cropped_image.height:
            direction = 'horizontal'
        else:
            direction = 'vertical'
        print(f'Direction: {direction}')
        # endregion

        # # region 5. Translate to modern Vietnamese
        # text = translate_to_modern_vietnamese(text)
        # # endregion


        # region 5. Create rectangle
        # draw.rectangle(
        #     xy = (tl, br),
        #     fill = bg_color
        # )
        draw.polygon(
            xy=(tl, tr, br, bl),
            fill = bg_color
        )
        # endregion
        
        if direction == 'horizontal':
            draw_text_horizontal(
                text  = text,
                direction= 'horizontal',
                bbox= (tl, br),
                draw= draw,
                fg_color= fg_color
            )
        else:
            # region get position for each word
            len_text  = len(text.split())
            padding = 2
            kc = cropped_image.height// len_text
            w = cropped_image.width

            bboxes = []
            sizes = []
            _tl = tl
            for _ in range(len_text):
                _br = (_tl[0]+ w, _tl[1]+ kc - padding)
                bbox_word = (_tl, _br)
                bbox_horizontal, size = check_bbox_is_horizontal_rectangle(bbox_word)
                bboxes.append(bbox_horizontal)
                sizes.append(size)
                _tl = (_tl[0], _tl[1]+ kc + padding)
            # endregion

            # region Get min text size
            lst_font_size = []
            lst_text = text.split()

            for bbox, text, (height, width) in zip(bboxes, lst_text, sizes):
                _, _, font_size= check_text_size(
                    text_string= text,
                    direction= 'horizontal',
                    width= width,
                    height= height
                )
                lst_font_size.append(font_size)

            font_size = min(lst_font_size)
            # endregion
            
            # Xac dinh va viet tung chu vao
            for bbox, text in zip(bboxes, lst_text):
                draw_text_vertical(
                    text = text,
                    bbox = bbox,
                    draw = draw,
                    fg_color= fg_color,
                    font_size= font_size
                )
    return pil_image
