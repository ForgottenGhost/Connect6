import random
import copy
import pygame,pygame.gfxdraw
from pygame.locals import *

class Board:
    def __init__(self,size,win_length):
        self.background = Color(26,153,0)
        self.line_width = 3
        self.box_width = 5
        self.size = size
        self.win_length = win_length
        self.contain = [[0 for idx in xrange(self.size)] for jdx in xrange(self.size)]
        self.selected_list = [(size/2,size/2),(size/2,size/2)]
        self.surface_size = None
        self.piece_size = None
        self.gap = None
        self.surface = None
        self.empty_loc_list = [[x,y] for x in xrange(self.size) for y in xrange (self.size) if self.contain[y][x] == 0]

    def get_empty_loc_list(self):
        return self.empty_loc_list

    def update_empty_loc_list(self,loc):
        self.empty_loc_list.remove(loc)

    def is_empty(self,loc):
        if loc in self.empty_loc_list:
            return True
        else:
            return False

    def play_piece(self,player):
        if player == 1:
            selected = self.selected_list[0]
        elif player == -1:
            selected = self.selected_list[1]
        if self.is_empty(selected):
            self.contain[selected[1]][selected[0]] = player
            self.update_empty_loc_list(selected)
            return True
        else:
            return False

    def c_selecting(self,player,selecting):
        if player == 1:
            self.selected_list[0] = selecting
        elif player == -1:
            self.selected_list[1] = selecting


    def p_selecting(self,changing):
        # This is where comments go so I don't have to ask so many questions
        self.selected_list = [[self.selected_list[0][0]+changing[0][0],self.selected_list[0][1]+changing[0][1]],
        [self.selected_list[1][0]+changing[1][0],self.selected_list[1][1]+changing[1][1]]]
        for idx in xrange(len(self.selected_list)):
            for jdx in xrange(len(self.selected_list[idx])):
                if self.selected_list[idx][jdx] < 0:
                    self.selected_list[idx][jdx] = 0
                elif self.selected_list[idx][jdx] > self.size-1:
                    self.selected_list[idx][jdx] = self.size-1
        return [[0,0],[0,0]]

    def count_board(self):
        sum_list = [sum(self.contain[y][x:x+self.win_length]) for y in xrange(self.size) for x in xrange(self.size-self.win_length+1) if self.contain[y][x] != 0]
        sum_list += [sum([self.contain[y+idx][x] for idx in xrange(self.win_length)]) for y in xrange(self.size-self.win_length+1) for x in xrange(self.size) if self.contain[y][x] != 0]
        sum_list += [sum([self.contain[y+idx][x+idx] for idx in xrange(self.win_length)]) for y in xrange(self.size-self.win_length+1) for x in xrange(self.size-self.win_length+1) if self.contain[y][x] != 0]
        sum_list += [sum([self.contain[y+idx][x-idx] for idx in xrange(self.win_length)]) for y in xrange(self.size-self.win_length+1) for x in xrange(self.win_length-1,self.size) if self.contain[y][x] != 0]
        return sum_list

    def check_win(self):
        sum_list = self.count_board()
        if self.win_length in sum_list:
            return 1
        elif -self.win_length in sum_list:
            return -1
        elif len(self.empty_loc_list) == 0:
            return -11
        else:
            return 0

    def draw(self,surface_size):
        if self.surface == None or self.surface != surface_size:
            self.surface_size = surface_size
            self.surface = pygame.Surface((self.surface_size, self.surface_size))
            self.piece_size = int(self.surface_size/(2.0*self.size))-2
            self.gap = (self.surface_size-(2.0*self.piece_size))/(self.size-1)
        self.surface.fill(self.background)
        for idx in xrange(self.size+1):
            pygame.draw.aaline(self.surface, Color(0,0,0), (self.piece_size + (idx*self.gap),self.piece_size), (self.piece_size + (idx*self.gap),self.surface_size - self.piece_size), self.line_width)
            pygame.draw.aaline(self.surface, Color(0,0,0), (self.piece_size,self.piece_size + (idx*self.gap)), (self.surface_size - self.piece_size,self.piece_size + (idx*self.gap)), self.line_width)
        piece_list = [(self.piece_size + (x*self.gap),self.piece_size + (y*self.gap),self.contain[x][y])for x in xrange(self.size) for y in xrange(self.size) if self.contain[x][y] != 0]
        for piece in piece_list:
            if piece[2] == 1:
                color = Color(0,0,0)
            elif piece[2] == -1:
                color = Color(255,255,255)
            pygame.gfxdraw.aacircle(self.surface, int(piece[1]), int(piece[0]), self.piece_size, color)
            pygame.gfxdraw.filled_circle(self.surface, int(piece[1]), int(piece[0]), self.piece_size, color)
        if self.selected_list[0] != self.selected_list[1]:
            for idx in xrange(len(self.selected_list)):
                pygame.draw.rect(self.surface,Color(idx*255,idx*255,idx*255),
                ((self.selected_list[idx][0]*self.gap,self.selected_list[idx][1]*self.gap),(self.piece_size*2,self.piece_size*2)),self.box_width)
        else:
            pygame.draw.rect(self.surface,Color(148,148,148),
            ((self.selected_list[0][0]*self.gap,self.selected_list[0][1]*self.gap),(self.piece_size*2,self.piece_size*2)),self.box_width)
        return self.surface

    def get_selecting(self):
        return self.selected_list

    def get_board_size(self):
        return self.size

    def get_board(self):
        return self.contain
