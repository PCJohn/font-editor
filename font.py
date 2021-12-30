import os
import glob
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps
from matplotlib import pyplot as plt

import tempfile
import fontTools
from fontTools.ttLib import TTFont

import constants


class Font:
    def __init__(self, ttf_file, font_size=112, disp_size=1000, bkg_col=(255,255,255), txt_col=(0,0,0)):
        self.font_size = font_size
        self.ttf_file = ttf_file
        self.pil_font = ImageFont.truetype(ttf_file, size=self.font_size)
        self.font = TTFont(ttf_file)
        self.glyphset = self.font.getGlyphSet()
        self.charset = list(self.glyphset.keys())

        # Variables to display characters
        self.im_size = disp_size
        self.bkg_col = bkg_col
        self.txt_col = txt_col
        self.img = Image.new('RGB', (self.im_size, self.im_size), color=bkg_col)
        self.canvas = ImageDraw.Draw(self.img)

    
    # Apply a transform to all supported characters
    def apply_transform(self, mat):
        for ch in self.charset:
            glyph = self.glyphset[ch]._glyph
            if 'coordinates' in dir(glyph):
                glyph.coordinates.transform(mat)
                #import pdb; pdb.set_trace();
        # Update PIL font to display: save and load back from temp file
        with tempfile.NamedTemporaryFile() as tmp:
            self.font.save(tmp)
            self.pil_font = ImageFont.truetype(tmp.name, size=self.font_size)


    # Update self.img with rendering of text using the font
    def display(self, txt, n_rows=1):
        (font_w, font_h), (font_offset_x, font_offset_y) = self.pil_font.font.getsize(txt)
        self.canvas.rectangle((0, 0, self.img.size[0], self.img.size[1]), fill=self.bkg_col) # clear canvas
        chunk_size = len(txt) // n_rows
        txt_chunks = [txt[i:(i+chunk_size)] for i in range(0,len(txt),chunk_size)]
        for i,chunk in enumerate(txt_chunks):
            self.canvas.text((-font_offset_x,font_h*i-font_offset_y), chunk, fill=self.txt_col, font=self.pil_font)
        #self.img = self.img.crop((0, 0, (font_w+1) //n_rows, font_h*n_rows))



if __name__ == '__main__':
    ttf_file = 'NotoSans-Regular.ttf'
    style_font = Font(ttf_file)

    font = Font(ttf_file)
    
    #font.display('abcdefghऄइईउऊऋऌऍ', n_rows=2); plt.imshow(font.img); plt.show()
    
    #font.apply_transform([[1,0],[0.6,1]])
    
    #font.display('abcdefghऄइईउऊऋऌऍ', n_rows=2); plt.imshow(font.img); plt.show()
   

    # Test -- try to increase thickness of the font
    for ch in font.charset[23:]:
        glyph = font.glyphset[ch]._glyph
        if 'coordinates' in dir(glyph):
            #coords = glyph.coordinates
            #contour_start = 0
            #for contour_idx in range(glyph.numberOfContours):
            #    contour_end = glyph.endPtsOfContours[contour_idx]
            #for i in range(coordinates):
            #    prev = 
            coords = glyph.coordinates[:]
            plt.scatter([x for (x,y) in coords], [y for (x,y) in coords])
            plt.show()
            import pdb; pdb.set_trace();

    #font.display('abcdefghऄइईउऊऋऌऍ', n_rows=2); plt.imshow(font.img); plt.show()



