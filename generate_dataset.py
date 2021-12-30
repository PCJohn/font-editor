import os
import glob
import string
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
from fontTools.ttLib import TTFont


class Font:
    def __init__(self, ttf_file):
        self.pil_font = ImageFont.truetype(ttf_file,size=225)
        fonttools_font = TTFont(ttf_file)
        self.supported_chars = [chr(t) for table in fonttools_font['cmap'].tables for t in table.cmap.keys()][:150]
    
    def getsize(self, txt):
        return self.pil_font.font.getsize(txt)

    def get_supported_chars(self,size=-1):
        if size == -1:
            return self.supported_chars
        np.random.shuffle(self.supported_chars)
        return self.supported_chars[:size]
    
    def display(self, txt, n_rows=1):
        im_h, im_w = (6556, 6556)
        (font_w, font_h), (font_offset_x, font_offset_y) = self.getsize(txt)
        img = Image.new('RGB', (im_h,im_w), color=(255,255,255))
        canvas = ImageDraw.Draw(img)
        chunk_size = len(txt) // n_rows
        txt_chunks = [txt[i:(i+chunk_size)] for i in range(0,len(txt),chunk_size)]
        for i,chunk in enumerate(txt_chunks):
            canvas.text((-font_offset_x,font_h*i-font_offset_y), chunk, fill=(0,0,0), font=self.pil_font)
        img = img.crop((0, 0, font_w, font_h))
        #img = img.crop((0, 0, font_w, font_h*n_rows))
        return img

    def display_char(self, ch):
        txt = str(ch)
        im_h, im_w = (6556, 6556)
        (font_w, font_h), (font_offset_x, font_offset_y) = self.getsize(txt)
        img = Image.new('RGB', (im_h,im_w), color=(255,255,255))
        canvas = ImageDraw.Draw(img)
        canvas.text((-font_offset_x,-font_offset_y), txt, fill=(0,0,0), font=self.pil_font)
        img = img.crop((0, 0, font_w, font_h))
        return img



def load_fonts(font_dir):
    fonts = [ Font(os.path.join(font_dir,ttf_file)) for ttf_file in os.listdir(font_dir) ]
    return fonts


def compare_fonts(font1, font2, n_chars=1):
    common_chars = list(set(font1.supported_chars) & set(font2.supported_chars))
    comparison_images = []
    for _ in range(n_chars):
        ch = np.random.choice(common_chars)
        im1 = font1.display_char(ch)
        im2 = font2.display_char(ch)
        comparison_images.append((im1,im2))
    return comparison_images


if __name__ == '__main__':

    fonts = load_fonts('/home/prithvi/data/fonts')
    #rand_font = np.random.choice(fonts)
    #img = rand_font.display('abcdef', n_rows=2)
    
    font1 = np.random.choice(fonts)
    font2 = np.random.choice(fonts)
    font_imgs = compare_fonts(font1, font2, n_chars=10)
    for im1,im2 in font_imgs:
        plt.subplot(121)
        plt.imshow(im1)
        plt.subplot(122)
        plt.imshow(im2)
        plt.show()




