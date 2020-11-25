import pygame as pg
import string
 
class TextBox(object):
    def __init__(self,rect,**kwargs):
        self.rect = pg.Rect(rect)
        self.buffer = []
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.delete_timer = 0.0
        self.accepted = string.ascii_letters+string.digits+string.punctuation+" "
        self.process_kwargs(kwargs)
 
    def process_kwargs(self,kwargs):
        defaults = {"id" : None,
                    "command" : None,
                    "active" : True,
                    "color" : (235, 238, 240),
                    "font_color" : pg.Color("black"),
                    "outline_color" : pg.Color("black"),
                    "outline_width" : 0,
                    "active_color" : pg.Color("blue"),
                    "font" : pg.font.Font('./twitter_emotions/models/font_family/GothamNarrow-Light.otf', 18),
                    "clear_on_enter" : False,
                    "inactive_on_enter" : True,
                    "blink_speed": 500,
                    "delete_speed": 75}
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("TextBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)
 
    def get_event(self,event, mouse_pos=None):
        ''' Call this on your event loop
         
            for event in pg.event.get():
                TextBox.get_event(event)
        '''
        if event.type == pg.KEYDOWN and self.active:
            if event.key in (pg.K_RETURN,pg.K_KP_ENTER):
                self.execute()
            elif event.key == pg.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
            elif event.unicode in self.accepted:
                self.buffer.append(event.unicode)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if not mouse_pos:
                mouse_pos = pg.mouse.get_pos()
            self.active = self.rect.collidepoint(mouse_pos)
 
    def execute(self):
        if self.command:
            self.command(self.id,self.final)
        self.active = not self.inactive_on_enter
        if self.clear_on_enter:
            self.buffer = []
             
    def set_buffer(self, text):
        self.buffer = text

    def switch_blink(self):
        if pg.time.get_ticks()-self.blink_timer > self.blink_speed:
            self.blink = not self.blink
            self.blink_timer = pg.time.get_ticks()
 
    def update(self):
        '''
        Call once on your main game loop
        '''
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            self.rendered = self.font.render(self.final, True, self.font_color)
            self.render_rect = self.rendered.get_rect(x=self.rect.x+2,
                                                      centery=self.rect.centery)
            if self.render_rect.width > self.rect.width-6:
                offset = self.render_rect.width-(self.rect.width-6)
                self.render_area = pg.Rect(offset,0,self.rect.width-6,
                                           self.render_rect.height)
            else:
                self.render_area = self.rendered.get_rect(topleft=(0,0))
        self.switch_blink()
        self.handle_held_backspace()
         
    def handle_held_backspace(self):
        if pg.time.get_ticks()-self.delete_timer > self.delete_speed:
            self.delete_timer = pg.time.get_ticks()
            keys = pg.key.get_pressed()
            if keys[pg.K_BACKSPACE]:
                if self.buffer:
                    self.buffer.pop()
 
    def draw(self,surface):
        '''
        Call once on your main game loop
        '''
        outline_color = self.active_color if self.active else self.outline_color
        outline = self.rect.inflate(self.outline_width*2,self.outline_width*2)
        surface.fill(outline_color,outline)
        surface.fill(self.color,self.rect)
        if self.rendered:
            surface.blit(self.rendered,self.render_rect,self.render_area)
        #if self.blink and self.active:
        #    curse = self.render_area.copy()
        #    curse.topleft = self.render_rect.topleft
        #    surface.fill(self.font_color,(curse.right+1,curse.y,2,curse.h))
        
#pg.init()
#screen = pg.display.set_mode((600,400))
#done = False
 
def name_on_enter(id, final):
    print('enter pressed, username is "{}"'.format(final))
     
 
username_settings = {
    "command" : name_on_enter,
    "inactive_on_enter" : False,
}
 
name_entry = TextBox(rect=(70,100,150,30), **username_settings)

 
#while not done:
#    for event in pg.event.get():
#        if event.type == pg.QUIT:
#            done = True
#        name_entry.get_event(event)
#    name_entry.update()
#    name_entry.draw(screen)
#    pg.display.update()