import math
def rotate_bounding_box(bounding_box, angle):
    """Rotates a bounding box around its center by the given angle.

    Args:
        bounding_box: A list of four numbers, representing the coordinates of the
        bounding box corners in the order [top left, top right, bottom right,
        bottom left].
        angle: The angle of rotation in degrees.

    Returns:
        A list of four numbers, representing the coordinates of the rotated bounding
        box corners.
    """
    tl = bounding_box[0]
    br = bounding_box[2]
    x1, y1 = tl
    x2, y2 = br
    cen_x  =x1 + (x2 - x1) //2
    cen_y = y1 + (y2 - y1) //2
    print(cen_x, cen_y)
    center = (cen_x, cen_y)
    rotated_center = rotate_point(center, angle)

    rotated_corners = [
        rotate_point(bounding_box[i], angle) for i in range(4)
    ]

    return [rotated_corners[0], rotated_corners[1], rotated_corners[2],
            rotated_corners[3]]

def rotate_point(point, angle):
  """Rotates a point around the origin by the given angle.

  Args:
    point: A list of two numbers, representing the coordinates of the point.
    angle: The angle of rotation in degrees.

  Returns:
    A list of two numbers, representing the coordinates of the rotated point.
  """

  x, y = point
  radians = angle * math.pi / 180
  new_x = x * math.cos(radians) - y * math.sin(radians)
  new_y = x * math.sin(radians) + y * math.cos(radians)

  return [new_x, new_y]

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

    second = (x_br, y_tl)
    fourth = (x_tl, y_br)

    return ((x_tl, y_tl), second, (x_br, y_br), fourth)
if __name__ == "__main__":
    x = ((233, 60), (264, 98))
    print(rotate_vertical_bbox_rectange(bbox=x))
    
    