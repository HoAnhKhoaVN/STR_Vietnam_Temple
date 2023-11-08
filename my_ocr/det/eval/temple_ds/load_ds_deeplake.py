import os
import deeplake
import pickle

class ICDAR_2013(object):
    def __init__(self, plk_name= 'icdar-2013-text-localize-test.plk'):
        self.plk_name = plk_name
        # self.data = self.read_ds()
        self.data = self.load_ds()
    
    def load_ds(self):
        print(f'--> Load icdar-2013-text-localize-test')
        ds = deeplake.load("hub://activeloop/icdar-2013-text-localize-test")
        return ds
        # print(ds)
        
        # print(f'--> Dump icdar-2013-text-localize-test')
        # with open(self.plk_name, 'wb') as f:
        #     pickle.dump(ds, f)

    def read_ds(self):
        if not os.path.exists(self.plk_name):
            print(f'==== LOAD DS FROM DEEPLAKE =====')
            self.load_ds()
        with open(self.plk_name, 'rb') as f:
            data = pickle.load(f)
        return data

    def get_bbox(self):
        print(self.data['boxes/box'][0])

    def get_label(self):
        print(self.data['boxes/label'])

    def get_img(self):
        print(self.data['images'])


if __name__ == '__main__':
    ds = ICDAR_2013()
    ds.get_bbox()
    # ds.get_img()
    # ds.get_label()