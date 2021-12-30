import tkinter
import tkinter.filedialog
import pygame
import math
import random
from pygame.locals import *

# Local imports
from font import Font
import constants


# Take colors input
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)


#Construct the GUI game
pygame.init()

#Set dimensions of game GUI
w, h = 1000, 1000
screen = pygame.display.set_mode((w, h))

# Set running, angle and scale values
running = True
angle = 0
scale = 1


display_font = pygame.font.SysFont('Arial', 30)
b1 = display_font.render('Rotate', False, (0, 0, 0))
b2 = display_font.render('Scale', False, (0, 0, 0))
text_save = display_font.render('Save', False, (0, 0, 0))


def save_box():
    top = tkinter.Tk()
    top.withdraw()
    #file_name = tkinter.filedialog.askopenfilename(parent=top)
    file_name = tkinter.filedialog.asksaveasfilename(parent=top)
    top.destroy()
    return file_name


def render_font(font):
    return pygame.image.fromstring(font.img.tobytes(), font.img.size, font.img.mode)



if __name__ == '__main__':
    # Take image as input
    disp_langs = [ 'english', 'hindi', 'greek', 'special' ]
    disp_chars_per_lang = 9
    disp_buffer = ' ' * 2 * disp_chars_per_lang
    disp_txt = disp_buffer + ' '.join([ ' '.join(random.sample(constants.CHARS_PER_LANG[lang], disp_chars_per_lang)) for lang in disp_langs ])
    disp_row = 5
    base_font = Font('NotoSans-Regular.ttf', font_size=112, disp_size=1000, bkg_col=(255,255,255), txt_col=(0,0,0))
    base_font.display(disp_txt, n_rows=disp_row)

    img = render_font(base_font)
    rect = img.get_rect()

    # Draw a rectangle around the image

    # Set the center and mouse position
    center = w // 2, h // 2
    mouse = pygame.mouse.get_pos()

    #Store the image in a new variable
    #Construct the rectangle around image
    rect.center = center

    sprites = pygame.sprite.Group()

    # Setting what happens when game is
    # in running state

    # State variables
    edit_action = 'none'
    mouse_down = False
    prev_angle = 90
    prev_scale = 1
    

    rect1 = pygame.Rect((0, 0), (108, 36))
    rect2 = pygame.Rect((124, 0), (108, 36))
    button_save = pygame.Rect((248, 0), (108, 36))

    while running:
        for event in pygame.event.get():
            # Close if the user quits the game
            if event.type == QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = event.pos
                if rect1.collidepoint(mouse):
                    edit_action = 'rotate'
                elif rect2.collidepoint(mouse):
                    edit_action = 'scale'
                elif button_save.collidepoint(mouse):
                    edit_action = 'none'
                    save_path = save_box()
                    if save_path:
                        base_font.font.save(save_path)
                mouse_down = True

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse = event.pos
                x = mouse[0] - center[0]
                y = mouse[1] - center[1]
                d = math.sqrt(x ** 2 + y ** 2)
                angle = math.degrees(-math.atan2(y, x))
                scale = abs(2 * d / w)
                
                if edit_action.lower() == 'rotate' and mouse_down:
                    if not rect1.collidepoint(mouse):
                        angle_delta = angle - prev_angle
                        cos = math.cos(math.radians(-angle_delta))
                        sin = math.sin(math.radians(-angle_delta))
                        M = [[cos, -sin], [sin, cos]]
                        base_font.apply_transform(M)
                        base_font.display(disp_txt, n_rows=disp_row)
                        img = render_font(base_font)
                        prev_angle = angle

                elif edit_action.lower() == 'scale' and mouse_down:
                    if not rect2.collidepoint(mouse):
                        scale_delta = scale / prev_scale
                        M = [[scale, 0], [0, scale]]
                        base_font.apply_transform(M)
                        base_font.display(disp_txt, n_rows=disp_row)
                        img = render_font(base_font)
                        prev_scale = scale

                rect = img.get_rect()
                rect.center = center
                
                mouse_down = False

        # Set screen color and image on screen
        screen.fill(WHITE, (0, 0, w, h))
        screen.blit(img, rect)

        # Display buttons
        rotate_col = LIGHT_GRAY
        if edit_action == 'rotate':
            rotate_col = DARK_GRAY
        pygame.draw.rect(screen, rotate_col, rect1)
        screen.blit(b1, (14,0))
        pygame.draw.rect(screen, LIGHT_GRAY, rect2)
        screen.blit(b2, (140,0))
        pygame.draw.rect(screen, LIGHT_GRAY, button_save)
        screen.blit(text_save, (264,0))

        sprites.draw(screen)

        # Display reference line: center to mouse location
        if mouse_down and 'pos' in dir(event):
            pygame.draw.line(screen, (0,0,255), center, event.pos, 5)

        # Update the GUI game
        pygame.display.update()

    # Quit the GUI game
    pygame.quit()

