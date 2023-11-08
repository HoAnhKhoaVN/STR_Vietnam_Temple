from shapely.geometry import Polygon

polygon1 = Polygon([
                [
                    470,
                    36
                ],
                [
                    505,
                    36
                ],
                [
                    505,
                    71
                ],
                [
                    470,
                    71
                ]
            ])
polygon2 = Polygon([
                [
                    756,
                    25
                ],
                [
                    800,
                    25
                ],
                [
                    804,
                    660
                ],
                [
                    760,
                    661
                ]
            ])
intersect = polygon1.intersection(polygon2).area
union = polygon1.union(polygon2).area
iou = intersect / union
print(iou)  # iou = 0.5