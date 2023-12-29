# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 16:19:16 2023

@author: Zheng
"""

import pygame
import sys
import random

pygame.init()

screen_length=400
screen_width=400
center_length=int(screen_length/2)
center_width=int(screen_width/2)
screen=pygame.display.set_mode((screen_length,screen_width))
pygame.display.set_caption('Starfield Simulation')
clock=pygame.time.Clock()

class Star(pygame.sprite.Sprite):
    def __init__(self,x,y,z):
        super().__init__()
        self.x=x
        self.y=y
        self.z=z
        self.x2d=x/z*240
        self.y2d=y/z*240
        self.brightness=255
        self.r=2
        
    def draw(self):
        pygame.draw.circle(screen, (self.brightness,self.brightness,self.brightness), (self.x2d+center_length,self.y2d+center_width), self.r)
    
    def transform3to2(self):
        self.x2d=self.x/(self.z-cam_z)*240
        self.y2d=self.y/(self.z-cam_z)*240
        self.r=500/(self.z-cam_z)
        self.brightness=max(0,min(255,int(-0.5*(self.z-cam_z)+255)))
    
    def update(self):
        if self.z-cam_z<=0:
            self.z+=draw_distance
            self.x=random.randint(-500, 500)
            self.y=random.randint(-500, 500)
        self.transform3to2()
        
class Sky:
    def __init__(self):
        self.sky=pygame.sprite.Group()
        for _ in range(800):
            rx=random.randint(-500, 500)
            ry=random.randint(-500, 500)
            rz=random.randint(1, draw_distance)
            self.sky.add(Star(rx,ry,rz))
            
    def draw(self):
        for i in self.sky:
            if screen_length-center_length>=i.x2d>=-center_length and screen_width-center_width>=i.y2d>=-center_width:
                i.draw()
            
    def update(self):
        self.sky.update()

def show__text(text,pos):
    text_image=show_font.render(text, 1, (255,255,255))
    screen.blit(text_image, pos)
    
show_font = pygame.font.SysFont("monospace", 15)
draw_distance=1000
cam_z=0
cam_speed=15
sky=Sky()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    cam_z+=cam_speed
    sky.update()
    
    screen.fill((0,0,0))
    sky.draw()
    show__text(str(int(clock.get_fps())), (0,0))
    show__text(str(cam_z), (0,20))
    
    pygame.display.flip()
    clock.tick(30)