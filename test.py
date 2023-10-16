import os
from my_postprocess.postprocess import _postprocess

if __name__ == "__main__":

    # region Input
    list_dict_result = [{'bbox': [[117, 99], [217, 74], [284, 353], [184, 378]], 'text': 'Tĩnh Lan'}]
    # list_dict_result=  [{'bbox': [[17, 154], [684, 146], [686, 362], [19, 369]], 'text': 'Quang Tiền Địch'}]
    # list_dict_result=  [{'bbox': [[245, 8], [293, 11], [256, 614], [209, 612]], 'text': 'Hiện Thế Vi Nhất Sư Đương Lai Tác Phật Tô'}, {'bbox': [[747, 16], [790, 18], [774, 576], [730, 575]], 'text': 'Hữu Thiền Hữu Tịnh Thổ Hoành Như Dải Giác Hổ'}]
    TGT = 'rotation/'
    image_path = 'input/366641616_2264556887067173_1651877982799532575_n.jpg'
    # image_path = 'input/365277540_2640178542812959_3109842896588336028_n.jpg'
    # image_path = "input/cau_doi_1.jpg"
    
    # endregion

    # region postprocessing
    res_img = _postprocess(
        image_fn= image_path,
        list_dict_result= list_dict_result
    )
    res_img.save(os.path.join(TGT, "cau_doi_1_demo.jpg"))



    # endregion

    
    