import os
import glob
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps
from matplotlib import pyplot as plt

import torch
import torch.nn as nn
from torchvision import transforms




class Font:
    def __init__(self, ttf_file):
        self.ttf_file = ttf_file
        self.pil_font = ImageFont.truetype(ttf_file,size=225)
    
    def getsize(self, txt):
        return self.pil_font.font.getsize(txt)
    
    def display_char(self, ch):
        txt = str(ch)
        im_h, im_w = (6556, 6556)
        (font_w, font_h), (font_offset_x, font_offset_y) = self.getsize(txt)
        img = Image.new('RGB', (im_h,im_w), color=(255,255,255))
        canvas = ImageDraw.Draw(img)
        canvas.text((-font_offset_x,-font_offset_y), txt, fill=(0,0,0), font=self.pil_font)
        img = img.crop((0, 0, font_w, font_h))
        img = ImageOps.grayscale(img)
        return img



if __name__ == '__main__':

    transform = transforms.Compose([transforms.Resize((64,64)),
                                    transforms.ToTensor(),
                                    transforms.Normalize(mean=(0.5),std=(0.5))])

    ### demo with english-chinese preprocessed dataset
    #style_fonts = '/home/prithvi/code/fonts/font_translator_gan/datasets/font/test_unknown_style/chinese/Fashionable dress Guang xin CU hei Font - Simplified Chinese/'
    #style_font_files = glob.glob(os.path.join(style_fonts,'*'))
    #style_imgs = torch.cat([transform(Image.open(font_file)) for font_file in style_font_files[:6]])
    #style_imgs = style_imgs.unsqueeze(0).cuda()
    #content_font_file = '/home/prithvi/code/fonts/font_translator_gan/datasets/font/test_unknown_style/english/Banner Bold Figure Chinese Font-Traditional Chinese Fonts/a.png'
    #content_font_file = '/home/prithvi/code/fonts/font_translator_gan/datasets/font/test_unknown_style/english/Banner Bold Figure Chinese Font-Traditional Chinese Fonts/a.png'
    #content_img = transform(Image.open(content_font_file))
    #content_img = content_img.unsqueeze(0).cuda()
    ###

    ### demo with google fonts
    #style_font = Font('/home/prithvi/data/fonts/google_fonts/ofl/galada/Galada-Regular.ttf')
    #style_font = Font('/home/prithvi/data/fonts/google_fonts/ofl/niramit/Niramit-LightItalic.ttf')
    #style_font = Font('/home/prithvi/data/fonts/google_fonts/ofl/mogra/Mogra-Regular.ttf')
    #style_font = Font('/home/prithvi/data/fonts/google_fonts/ofl/milonga/Milonga-Regular.ttf')
    #style_font = Font('/home/prithvi/data/fonts/google_fonts/ofl/nosifer/Nosifer-Regular.ttf')
    #style_font = Font('/home/prithvi/data/fonts/google_fonts/ofl/salsa/Salsa-Regular.ttf')
    style_font = Font('/home/prithvi/Desktop/Christmas Hat.ttf')
    
    style_imgs = torch.cat([ transform(style_font.display_char(ch)) for ch in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789?+=[]{}' ])
    style_imgs = style_imgs.unsqueeze(0).cuda()
    #content_font = Font('/home/prithvi/data/fonts/google_fonts/ofl/lohittamil/Lohit-Tamil.ttf')
    #content_img = transform(content_font.display_char(np.random.choice(['௷','௧','௹','௴','௳','ௐ','ழ்','த','மி'])))
    #content_font = Font('/home/prithvi/data/fonts/google_fonts/ofl/hind/Hind-Regular.ttf')
    content_font = Font('/home/prithvi/data/fonts/google_fonts/ofl/hind/Hind-Light.ttf')
    content_img = transform(content_font.display_char(np.random.choice(['क','ख','ग','घ','फ','श'][-1:])))
    content_img = content_img.unsqueeze(0).cuda()
    ###
    print('>>>',style_imgs.shape, content_img.shape)

    
    #style_imgs = torch.stack([transform(Image.open(font_file).convert('RGB')) for font_file in style_font_files[:5]])
    #content_img = transform(Image.open(content_font_file).convert('RGB'))
    
    print(style_imgs.shape, content_img.shape)
    
    #model_path = '/home/prithvi/code/fonts/font_translator_gan/checkpoints/test_new_dataset/20_net_G.pth'  #latest_net_G.pth'
    model_path = '/home/prithvi/code/fonts/font_translator_gan/checkpoints/google_fonts_no_aug/200_net_G.pth'

    import demo_model
    num_style_imgs = len(style_imgs)
    model = demo_model.define_G(num_style_imgs+1, 1, 32, 'FTGAN_MLAN', 'batch', True).cuda()
    #self.style_channel+1, 1, opt.ngf, opt.netG, opt.norm, not opt.no_dropout, opt.init_type, opt.init_gain, self.gpu_ids

    model.load_state_dict(torch.load(model_path))
    model.eval()
    #model = model.to('cpu')

    #import pdb; pdb.set_trace();
    pred = model([content_img, style_imgs], ensemble=True)

    plt.subplot(131)
    plt.imshow(content_img[0,0].cpu().detach().numpy(), cmap='gray')
    #plt.imshow(content_img[0,0].detach().numpy(), cmap='gray')
    plt.subplot(132)
    plt.imshow(style_imgs[0,0].cpu().detach().numpy(), cmap='gray')
    #plt.imshow(style_imgs[0,0].detach().numpy(), cmap='gray')
    plt.subplot(133)
    p = pred[0,0].cpu().detach().numpy() * 0.5 + 0.5
    #print(p.mean(),p.std(),p.max(),p.min())
    #p /= p.max()
    #p[p<0.2] = 0
    #p[p>0.2] = 1
    plt.imshow(p, cmap='gray')
    #plt.imshow(pred[0,0].detach().numpy(), cmap='gray')
    plt.show()
    #import pdb; pdb.set_trace();


    #model = create_model(opt)      # create a model given opt.model and other options
    #model.eval()
    #data = transform(img)
    #out = model(data)


