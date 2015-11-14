#
# This file is where you make the display for your game
# Make changes and add functions as you need.
#
import os
import pygame
from config import *
from common.event import *
from client.base_display import BaseDisplay


class Display(BaseDisplay):
    """
    This class controls all of the drawing of the screen
    for your game.  The process of drawing a screen is
    to first draw the background, and then draw everything
    that goes on top of it.  If two items are drawn in the
    same place, then the last item drawn will be the one
    that is visible.

    The screen is a 2 dimensional grid of pixels, with the
    origin (0,0) located at the top-left of the screen, and
    x values increase to the right and y values increase as
    you go down.  The y values are opposite of what you learned
    in your math classes.

    Documentation on drawing in pygame is available here:
    http://www.pygame.org/docs/ref/draw.html

    The methods in this class are:
    __init__ creates data members (variables) that are used
        in the rest of the methods of this class.  This is
        useful for defining colors and sizes, loading image
        or sound files, creating fonts, etc.  Basically,
        any one time setup.

    paint_game controls the drawing of the screen while the
        game is in session.  This is responsible for making
        sure that any information, whether graphics, text, or
        images are drawn to the screen.

    paint_waiting_for_game controls the drawing of the screen
        after you have requested to join a game, but before
        the game actually begins.
    
    paint_game_over controls the drawing of the screen after
        the game has been won, but before the game goes away.
        This is a short (3-5 second) period.

    process_event controls handling events that occur in the
        game, that aren't represented by objects in the game
        engine.  This includes things like collisions,
        objects dying, etc.  This would be a great place to
        play an audio file when missiles hit objects.

    paint_pregame controls the drawing of the screen before
        you have requested to join a game.  This would usually
        allow the user to know the options available for joining
        games.

    Method parameters and data members of interest in these methods:
    self.width is the width of the screen in pixels.
    self.height is the height of the screen in pixels.
    self.* many data members are created in __init__ to set up
        values for drawing, such as colors, text size, etc.
    surface is the screen surface to draw to.
    control is the control object that is used to
        control the game using user input.  It may
        have data in it that influences the display.
    engine contains all of the game information about the current
        game.  This includes all of the information about all of
        the objects in the game.  This is where you find all
        of the information to display.
    event is used in process_event to communicate what
        interesting thing occurred.
    
    Note on text display:  There are 3 methods to assist
    in the display of text.  They are inherited from the
    BaseDisplay class.  See client/base_display.py.
    
    """

    def __init__(self, width, height):
        """
        Configure display-wide settings and one-time
        setup work here.
        """
        BaseDisplay.__init__(self, width, height)

        # There are other fonts available, but they are not
        # the same on every computer.  You can read more about
        # fonts at http://www.pygame.org/docs/ref/font.html
        self.font_size = 12
        self.font = pygame.font.SysFont("Courier New",self.font_size)

        # Colors are specified as a triple of integers from 0 to 255.
        # The values are how much red, green, and blue to use in the color.
        # Check out http://www.colorpicker.com/ if you want to try out
        # colors and find their RGB values.   Be sure to use the `R`, `G`,
        # `B` values at the bottom, not the H, S, B values at the top.
        self.player_color     = (0, 255, 0)
        self.opponent_color   = (255, 0, 0)
        self.missile_color    = (0, 255, 255)
        self.npc_color        = (100, 100, 100)
        self.wall_color       = (150, 75, 0)
        self.text_color       = (255, 255, 255)
        self.background_color = (40, 199, 15)
        return

    def paint_pregame(self, surface, control):
        """
        Draws the display before the user selects the game type.
        """
        # background
        rect = pygame.Rect(0, 0, self.width, self.height)
        surface.fill(self.background_color, rect)
        # text message in center of screen
        s = "Press 'm' for multi player, 's' for single player,"
        self.draw_text_center(surface, s, self.text_color,
                              self.width/2, self.height/2,
                              self.font)
        s = "'t' for tournament, 'esc' to quit."
        self.draw_text_center(surface, s, self.text_color,
                              self.width/2, self.height/2 + 3*self.font_size/2,
                              self.font)
        file_path = os.path.join('display', 'images', 'TitlePage.png')
        image = pygame.image.load(file_path)
        surface.blit(image, rect)

        return
        
    def paint_waiting_for_game(self, surface, engine, control):
        """
        Draws the display after user selects the game type, before the game begins.
        This is usually a brief period of time, while waiting for an opponent
        to join the game.
        """
        # background
        rect = pygame.Rect(0, 0, self.width, self.height)
        surface.fill(self.background_color, rect)
        # text message in center of screen
        s = "Loading game..."
        self.draw_text_center(surface, s, self.text_color,
                              self.width/2, self.height/2,
                              self.font)
        return

    def paint_game(self, surface, engine, control):
        """
        Draws the display after the game starts.
        """
        # background
        rect = pygame.Rect(0, 0, self.width, self.height)
        surface.fill(self.background_color, rect)

        # Set a random bg color
        if hasattr(control, 'background_color') and control.background_color != self.background_color:
            self.background_color = control.background_color
        # draw each object
        objs = engine.get_objects()
        for key in objs:
            obj = objs[key]
            if obj.is_wall():
                self.paint_wall(surface, engine, control, obj)
            elif obj.is_npc():
                self.paint_npc(surface, engine, control, obj)
            elif obj.is_missile():
                self.paint_missile(surface, engine, control, obj)
            elif obj.is_player():
                self.paint_player(surface, engine, control, obj)
            else:
                print "Unexpected object type: %s" % (str(obj.__class__))
                
        # draw game data
        if control.show_info:
            self.paint_game_status(surface, engine, control)
        return

        
    def paint_game_over(self, surface, engine, control):
        """
        Draws the display after the game ends.  This
        chooses to display the game, and add a game over
        message.
        """
        self.paint_game(surface, engine, control)
        
        s = "Game Over (%s wins!)" % (engine.get_winner_name())
        self.draw_text_center(surface, s, self.text_color, int(self.width/2), int(self.height/2), self.font)
        return

    def process_event(self, surface, engine, control, event):
        """
        Should process the event and decide if it needs to be displayed, or heard.
        """
        return

    # The following methods draw appropriate rectangles
    # for each of the objects, by type.
    # Most objects have an optional text display to
    # demonstrate how to send information from the control
    # to the display.
    def paint_wall(self, surface, engine, control, obj):
        """
        Draws walls.
        """
        rect = self.obj_to_rect(obj)
        pygame.draw.rect(surface, self.wall_color, rect)
        return
        
    def paint_npc(self, surface, engine, control, obj):
        """
        Draws living NPCs.
        """
        if obj.is_alive():
            rect = self.obj_to_rect(obj)
            if obj.get_dx() > 0:
                npcpng = 'npc3.png'
            elif obj.get_dx() < 0:
                npcpng = 'npc4.png'
            elif obj.get_dy() > 0:
                npcpng = 'npc1.png'
            else:
                npcpng = 'npc2.png'
            file_path = os.path.join('display', 'images', npcpng)
            image = pygame.image.load(file_path)
            surface.blit(image, rect)

            pct = (obj.get_health() / obj.get_max_health()) * 10
            pct = int(round(pct))
            health = ''
            health = health.ljust(pct, chr(156))
            health = health.ljust(10)
            health = '|' + health + '|'
        else:
            health = 'LEVEL UP!'

        self.draw_text_center(surface, health, (200, 0, 0),
                              obj.get_x() + 2, obj.get_y() + 3.5,
                              self.font)
        return
        
    def paint_missile(self, surface, engine, control, obj):
        """
        Draws living missiles.
        """
        if obj.is_alive():
            obj.set_w(1.8)
            obj.set_h(1.8)
            rect = self.obj_to_rect(obj)
            file_path = os.path.join('display', 'images', 'Energy-Ball.png')
            image = pygame.image.load(file_path)
            surface.blit(image, rect)
        return
        
    def paint_player(self, surface, engine, control, obj):
        """
        Draws living players.
        My player is my opponent are in different colors
        """
        pct = (obj.get_health() / obj.get_max_health()) * 10
        pct = int(round(pct))
        health = ''
        health = health.ljust(pct, chr(156))
        health = health.ljust(10)
        health = '|' + health + '|'
        self.draw_text_center(surface, health, (200, 0, 0),
                              obj.get_x() + 2, obj.get_y() + 3.5,
                              self.font)
        if obj.is_alive():
            rect = self.obj_to_rect(obj)
            if obj.get_oid() == engine.get_player_oid():
                file_path = os.path.join('display', 'images', control.player_image)
            else: 
                if obj.get_dx() > 0:
                    enemyimg = 'enemy1.png'
                elif obj.get_dx() < 0:
                    enemyimg = 'enemy2.png'
                elif obj.get_dy() > 0:
                    enemyimg = 'enemy3.png'
                else:
                    enemyimg = 'enemy4.png'
                file_path = os.path.join('display', 'images', enemyimg)
            image = pygame.image.load(file_path)
            surface.blit(image, rect)
        return

    def paint_game_status(self, surface, engine, control):
        """
        This method displays some text in the bottom strip
        of the screen.  You can make it do whatever you want,
        or nothing if you want.
        """

        # display my stats
        oid = engine.get_player_oid()
        if oid > 0: 
            obj = engine.get_object(oid)
            if obj:
                s = "Me: %s  HP: %.1f  XP: %.1f Moving: %.1f Missiles: %.1f" % \
                    (engine.get_name(),
                     obj.get_health(),
                     obj.get_experience(),
                     obj.get_move_mana(),
                     obj.get_missile_mana())
                position_x = 20
                position_y = self.height - STATUS_BAR_HEIGHT + 3 * self.font_size / 1.5
                self.draw_text_left(surface, s, self.text_color, position_x, position_y, self.font)
                
        # display opponent's stats
        oid = engine.get_opponent_oid()
        if oid > 0: 
            obj = engine.get_object(oid)
            if obj:
                s = "Opponent: %s  HP: %.1f  XP: %.1f Moving: %.1f Missiles: %.1f" % \
                    (engine.get_opponent_name(),
                     obj.get_health(),
                     obj.get_experience(),
                     obj.get_move_mana(),
                     obj.get_missile_mana())
                position_x = 20
                position_y = self.height - STATUS_BAR_HEIGHT + 6 * self.font_size / 1.5
                self.draw_text_left(surface, s, self.text_color, position_x, position_y, self.font)
        return

