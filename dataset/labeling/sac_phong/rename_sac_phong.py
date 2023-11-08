import os
from tqdm import tqdm

IMG_PATH = 'sptn_figures'
TIEN_TO = [
    'sac_phong',
    'che_phong',
    'chieu'
]

VALID_RANGE = [
    range(0,70),
    range(70, 109),
    range(109,119)
]

OUT_SUBFORDER = [
    'sac_phong_trieu_nguyen_figure/sac_phong',
    'sac_phong_trieu_nguyen_figure/che_phong',
    'sac_phong_trieu_nguyen_figure/chieu'
]

def rename_prefix():
    for img_fn in tqdm(os.listdir(IMG_PATH), desc = 'Rename prefix: '):
        # print(f'img_fn : {img_fn}')
        # get name
        fn , ext = os.path.splitext(p = img_fn)
        # print(f'fn: {fn}')
        # print(f'ext: {ext}')
        # get page
        _, page_num, pos = fn.split('-')
        # print(f'page_num : {page_num}')
        # print(f'pos : {pos}')

        prefix = ''
        for idx, _range in enumerate(VALID_RANGE):
            if int(page_num) in _range:
                prefix = TIEN_TO[idx]
        # print(f'prefix: {prefix}')


        new_name = f'{prefix}-{page_num}-{pos}{ext}'
        # print(f'new_name: {new_name}')

        # Rename
        os.rename(
            src = os.path.join(IMG_PATH, img_fn),
            dst = os.path.join(IMG_PATH, new_name),
        )
        # break

def move_file():
    for img_fn in tqdm(os.listdir(IMG_PATH), desc = 'Move file: '):
        # print(f'img_fn : {img_fn}')
        # get name
        fn , ext = os.path.splitext(p = img_fn)
        # print(f'fn: {fn}')
        # print(f'ext: {ext}')
        # get page
        prefix, page_num, pos = fn.split('-')
        # print(f'page_num : {page_num}')
        # print(f'pos : {pos}')

        fd_path = ''
        for idx, _range in enumerate(VALID_RANGE):
            if int(page_num) in _range:
                fd_path = OUT_SUBFORDER[idx]
        # print(f'fd_path: {fd_path}')


        # new_name = f'{prefix}-{page_num}-{pos}{ext}'
        # print(f'new_name: {new_name}')

        # Rename
        src = os.path.join(IMG_PATH, img_fn)
        dst = os.path.join(fd_path, img_fn)
        os.system(
            f'mv {src} {dst}'
        )
        # break

def danh_so():
    for fd in OUT_SUBFORDER:
        for idx, img_fn in tqdm(enumerate(os.listdir(fd)), desc = f'Đánh số cho {fd}: '):
            # print(f'img_fn : {img_fn}')
            # get name
            fn , ext = os.path.splitext(p = img_fn)
            # print(f'fn: {fn}')
            # print(f'ext: {ext}')
            # get page
            prefix, page_num, pos = fn.split('-')
            # print(f'page_num : {page_num}')
                # print(f'pos : {pos}')
            new_name = f'{prefix}-{page_num}-{pos}-so{str(idx+1).zfill(3)}{ext}'
            # print(f'new_name: {new_name}')

            # Rename
            src = os.path.join(fd, img_fn)
            dst = os.path.join(fd, new_name)
            os.system(
                f'mv {src} {dst}'
            )
            # break
    # break


if __name__ == '__main__':
    rename_prefix()
    move_file()
    danh_so()


