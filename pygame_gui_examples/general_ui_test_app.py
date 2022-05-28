import random
import os
import pygame
import pygame_gui
from collections import deque

from pygame_gui import UIManager, PackageResource

from pygame_gui.elements import UIWindow
from pygame_gui.elements import UIButton
from pygame_gui.elements import UIHorizontalSlider
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UIDropDownMenu
from pygame_gui.elements import UIScreenSpaceHealthBar
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIImage
from pygame_gui.elements import UIPanel
from pygame_gui.elements import UISelectionList

from pygame_gui.windows import UIMessageWindow

import pygame


class ScalingWindow(UIWindow):  #창 만들기

    def __init__(self, rect, ui_manager):
        super().__init__(rect,
                         ui_manager,
                         window_display_title='Scale',
                         object_id='#scaling_window',
                         resizable=True)

        loaded_test_image = pygame.image.load(
            'data/images/splat.bmp').convert_alpha()
        self.test_image = UIImage(pygame.Rect(
            (10, 10), (self.get_container().get_size()[0] - 20,
                       self.get_container().get_size()[1] - 20)),
                                  loaded_test_image,
                                  self.ui_manager,
                                  container=self,
                                  anchors={
                                      'top': 'top',
                                      'bottom': 'bottom',
                                      'left': 'left',
                                      'right': 'right'
                                  })

        self.set_blocking(True)


class EverythingWindow(UIWindow):

    def __init__(self, rect, ui_manager):
        super().__init__(rect,
                         ui_manager,
                         window_display_title='Everything Container',
                         object_id='#everything_window',
                         resizable=True)

        self.slider_label = UILabel(
            pygame.Rect(
                (int(self.rect.width / 2) + 250, int(self.rect.height * 0.70)),
                (28, 25)),
            str(int(self.test_slider.get_current_value())),
            self.ui_manager,
            container=self)

        self.test_text_entry = UITextEntryLine(pygame.Rect(
            (int(self.rect.width / 2), int(self.rect.height * 0.50)),
            (200, -1)),
                                               self.ui_manager,
                                               container=self)
        self.test_text_entry.set_forbidden_characters('numbers')

        self.health_bar = UIScreenSpaceHealthBar(pygame.Rect(
            (int(self.rect.width / 9), int(self.rect.height * 0.7)),
            (200, 30)),
                                                 self.ui_manager,
                                                 container=self)
        '''loaded_test_image = pygame.image.load('data/images/splat.bmp').convert_alpha()

        self.test_image = UIImage(pygame.Rect((int(self.rect.width / 9),
                                               int(self.rect.height * 0.3)),
                                              loaded_test_image.get_rect().size),
                                  loaded_test_image, self.ui_manager,
                                  container=self)'''

    def update(self, time_delta):
        super().update(time_delta)

        if self.alive() and self.test_slider.has_moved_recently:
            self.slider_label.set_text(
                str(int(self.test_slider.get_current_value())))


class Options:

    def __init__(self):
        self.resolution = (1515, 850)
        self.fullscreen = False


class OptionsUIApp:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Mobility Model simulation")
        self.options = Options()
        if self.options.fullscreen:
            self.window_surface = pygame.display.set_mode(
                self.options.resolution, pygame.FULLSCREEN)
        else:
            self.window_surface = pygame.display.set_mode(
                self.options.resolution)

        self.background_surface = None

        self.ui_manager = UIManager(
            self.options.resolution,
            PackageResource(package='data.themes', resource='theme_2.json'))
        self.ui_manager.preload_fonts([{
            'name': 'fira_code',
            'point_size': 10,
            'style': 'bold'
        }, {
            'name': 'fira_code',
            'point_size': 10,
            'style': 'regular'
        }, {
            'name': 'fira_code',
            'point_size': 10,
            'style': 'italic'
        }, {
            'name': 'fira_code',
            'point_size': 14,
            'style': 'italic'
        }, {
            'name': 'fira_code',
            'point_size': 14,
            'style': 'bold'
        }])
        

        self.test_button = None
        self.test_button_2 = None
        self.test_button_3 = None
        self.test_slider = None
        self.test_text_entry = None
        self.test_drop_down = None
        self.test_drop_down_2 = None
        self.panel = None
        self.fps_counter = None
        self.frame_timer = None
        self.disable_toggle = None
        self.hide_toggle = None
        self.model = None
        self.deceleration = None

        self.message_window = None

        self.recreate_ui()

        self.clock = pygame.time.Clock()
        self.time_delta_stack = deque([])

        self.button_response_timer = pygame.time.Clock()
        self.running = True
        self.debug_mode = False

        self.all_enabled = True
        self.all_shown = True

    def recreate_ui(self):
        self.ui_manager.set_window_resolution(self.options.resolution)
        self.ui_manager.clear_and_reset()

        self.background_surface = pygame.Surface(self.options.resolution)
        self.background_surface.fill(self.ui_manager.get_theme().get_colour(
            ('dark_bg')))

        self.test_button = UIButton(
            pygame.Rect(
                (
                    int(self.options.resolution[0] /
                        2),  # click this button 만들기
                    int(self.options.resolution[1] * 0.90)),
                (180, 40)),
            'Simulation Start!',
            self.ui_manager)
        '''current_resolution_string = (str(self.options.resolution[0]) +
                                     'x' +
                                     str(self.options.resolution[1]))'''
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #---------------------------------------------------------왼쪽 프레임에 적어야할 input 값들---------------------------------------------------------------
        self.panel = UIPanel(
            pygame.Rect(10, 50, 310, 400),  #왼쪽 프레임
            starting_layer_height=4,
            manager=self.ui_manager)
        UILabel(pygame.Rect(70, 10, 174, 30),
                "[---Input values---]",
                manager=self.ui_manager,
                container=self.panel)
        UILabel(pygame.Rect(10, 45, 160, 20),
                "coverage map x :",
                manager=self.ui_manager,
                container=self.panel)
        self.tb_coverage_map_x = UITextEntryLine(pygame.Rect(195, 43, 80, 25),
                                                 self.ui_manager,
                                                 object_id='#main_text_entry',
                                                 container=self.panel)
        #self.test_text_entry.set_text_length_limit(3)
        self.tb_coverage_map_x.set_text('')
        UILabel(pygame.Rect(275, 45, 30, 20),
                "(m)",
                manager=self.ui_manager,
                container=self.panel)

        UILabel(pygame.Rect(10, 70, 160, 20),
                "coverage map y :",
                manager=self.ui_manager,
                container=self.panel)
        self.tb_coverage_map_y = UITextEntryLine(pygame.Rect(195, 67, 80, 25),
                                                 self.ui_manager,
                                                 object_id='#main_text_entry',
                                                 container=self.panel)
        #self.test_text_entry.set_text_length_limit(3)
        self.tb_coverage_map_y.set_text('')
        UILabel(pygame.Rect(275, 70, 30, 20),
                "(m)",
                manager=self.ui_manager,
                container=self.panel)

        UILabel(pygame.Rect(10, 95, 185, 20),
                "coverage map cell size:",
                manager=self.ui_manager,
                container=self.panel)
        self.tb_coverage_map_cell = UITextEntryLine(
            pygame.Rect(195, 91, 80, 25),
            self.ui_manager,
            object_id='#main_text_entry',
            container=self.panel)
        #self.test_text_entry.set_text_length_limit(3)
        self.tb_coverage_map_cell.set_text('')
        UILabel(pygame.Rect(275, 95, 30, 20),
                "(m)",
                manager=self.ui_manager,
                container=self.panel)

        UILabel(pygame.Rect(10, 120, 160, 20),
                "How many drone :",
                manager=self.ui_manager,
                container=self.panel)
        self.tb_drone_number = UITextEntryLine(pygame.Rect(195, 115, 80, 25),
                                               self.ui_manager,
                                               object_id='#main_text_entry',
                                               container=self.panel)
        #self.test_text_entry.set_text_length_limit(3)
        self.tb_drone_number.set_text('')
        UILabel(pygame.Rect(275, 120, 30, 20),
                "(n)",
                manager=self.ui_manager,
                container=self.panel)

        UILabel(pygame.Rect(10, 145, 160, 20),
                "UAV Minimum Rotation Radius :",
                manager=self.ui_manager,
                container=self.panel)
        self.tb_minimum_rotation = UITextEntryLine(
            pygame.Rect(195, 139, 80, 25),
            self.ui_manager,
            object_id='#main_text_entry',
            container=self.panel)
        #self.test_text_entry.set_text_length_limit(3)
        self.tb_minimum_rotation.set_text('')
        UILabel(pygame.Rect(275, 142, 30, 20),
                "(m)",
                manager=self.ui_manager,
                container=self.panel)

        UILabel(pygame.Rect(10, 170, 160, 20),
                "FOV(unit:angle) :",
                manager=self.ui_manager,
                container=self.panel)
        self.tb_FOV_angle = UITextEntryLine(pygame.Rect(195, 163, 80, 25),
                                            self.ui_manager,
                                            object_id='#main_text_entry',
                                            container=self.panel)
        #self.test_text_entry.set_text_length_limit(3)
        self.tb_FOV_angle.set_text('')
        UILabel(pygame.Rect(275, 165, 30, 20),
                "(°)",
                manager=self.ui_manager,
                container=self.panel)

        UILabel(pygame.Rect(10, 195, 160, 20),
                "UAV search height :",
                manager=self.ui_manager,
                container=self.panel)
        self.tb_search_height = UITextEntryLine(pygame.Rect(195, 187, 80, 25),
                                               self.ui_manager,
                                               object_id='#main_text_entry',
                                               container=self.panel)
        #self.test_text_entry.set_text_length_limit(3)
        self.tb_search_height.set_text('')
        UILabel(pygame.Rect(50, 250, 170, 20),
                "[UAV mobility model]",
                manager=self.ui_manager,
                container=self.panel)
        self.model = UIDropDownMenu(
            ['Random Waypoint model', 'RDPZ model', 'Pheromone Repel model'],
            'choice',
            pygame.Rect(50, 275, 175, 25),
            self.ui_manager,
            container=self.panel)
        UILabel(pygame.Rect(50, 300, 170, 20),
                "[UAV flight type]",
                manager=self.ui_manager,
                container=self.panel)
        self.deceleration = UIDropDownMenu(
            ['A Deceleration', 'NO Deceleration'],
            'choice',
            pygame.Rect(50, 325, 175, 25),
            self.ui_manager,
            container=self.panel)
        '''self.test_drop_down = UIDropDownMenu(['640x480', '800x600', '1500x850'],
                                             current_resolution_string,
                                             pygame.Rect((int(self.options.resolution[0] / 18),
                                                          int(self.options.resolution[1] * 0.8)),
                                                         (200, 25)),
                                             self.ui_manager)'''
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #-------------------------------------------------------이 GUI전체를 중지할지 숨길지 지정할 수 있는 버튼 생성---------------------------------------------------------
        self.disable_toggle = UIButton(pygame.Rect(
            (int(self.options.resolution[0] * 0.85),
             int(self.options.resolution[1] * 0.90)), (100, 30)),
                                       'Disable',
                                       self.ui_manager,
                                       object_id='#disable_button')

        self.hide_toggle = UIButton(pygame.Rect(
            (int(self.options.resolution[0] * 0.85),
             int(self.options.resolution[1] * 0.85)), (100, 30)),
                                    'Hide',
                                    self.ui_manager,
                                    object_id='#hide_button')
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------star버튼 누르면 simulation,graph 창 띄우는 설정--------------------------------------------------------------

    def create_message_window(self):
        self.button_response_timer.tick()
        graph_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((310, 39, 370, 750)),
            manager=self.ui_manager,
            resizable=False,
            window_display_title='Graph')

        graph_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((660, 39, 850, 750)),
            manager=self.ui_manager,
            resizable=False,
            window_display_title='simulation')
        '''background_image = pygame.image.load('data/images/MAP.png')
        bgimage=UIImage.set_image(background_image)
        self.test_image = UIImage(pygame.Rect(0,0, 850,750,
                                bgimage, manager=self.ui_manager))'''

        time_taken = self.button_response_timer.tick() / 1000.0
        # currently taking about 0.35 seconds down from 0.55 to create
        # an elaborately themed message window.
        # still feels a little slow but it's better than it was.
        print("Time taken to create message window: " + str(time_taken))
        print(self.tb_coverage_map_x.text) 
        print(self.tb_coverage_map_y.text)
        print(self.tb_coverage_map_cell.text)
        print(self.tb_drone_number.text)
        print(self.tb_minimum_rotation.text)
        print(self.tb_FOV_angle.text)
        print(self.tb_search_height.text)
        print(self.model.selected_option) 
        print(self.deceleration.selected_option)   


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def check_resolution_changed(self):
        resolution_string = self.test_drop_down.selected_option.split('x')
        resolution_width = int(resolution_string[0])
        resolution_height = int(resolution_string[1])
        if (resolution_width != self.options.resolution[0]
                or resolution_height != self.options.resolution[1]):
            self.options.resolution = (resolution_width, resolution_height)
            self.window_surface = pygame.display.set_mode(
                self.options.resolution)
            self.recreate_ui()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.ui_manager.process_events(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("self.ui_manager.focused_set:",
                      self.ui_manager.focused_set)

            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED
                    and event.ui_object_id == '#main_text_entry'):
                print(event.text)

            if event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
                if event.link_target == 'test':
                    print("clicked test link")
                elif event.link_target == 'actually_link':
                    print("clicked actually link")

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.test_button:
                    self.create_message_window()

                if event.ui_element == self.disable_toggle:
                    if self.all_enabled:
                        self.disable_toggle.set_text('Enable')
                        self.all_enabled = False
                        self.ui_manager.root_container.disable()
                        self.disable_toggle.enable()
                        self.hide_toggle.enable()
                    else:
                        self.disable_toggle.set_text('Disable')
                        self.all_enabled = True
                        self.ui_manager.root_container.enable()

                if event.ui_element == self.hide_toggle:
                    if self.all_shown:
                        self.hide_toggle.set_text('Show')
                        self.all_shown = False
                        self.ui_manager.root_container.hide()
                        self.hide_toggle.show()
                    else:
                        self.hide_toggle.set_text('Hide')
                        self.all_shown = True
                        self.ui_manager.root_container.show()

            if (event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
                    and event.ui_element == self.test_drop_down):
                self.check_resolution_changed()

    def run(self):
        while self.running:
            time_delta = self.clock.tick() / 1000.0
            self.time_delta_stack.append(time_delta)
            if len(self.time_delta_stack) > 2000:
                self.time_delta_stack.popleft()

            # check for input
            self.process_events()

            # respond to input
            self.ui_manager.update(time_delta)
            '''if len(self.time_delta_stack) == 2000:
                self.fps_counter.set_text(
                    f'FPS: {min(999.0, 1.0/max(sum(self.time_delta_stack)/2000.0, 0.0000001)):.2f}')
                self.frame_timer.set_text(f'frame_time: {sum(self.time_delta_stack)/2000.0:.4f}')'''

            # draw graphics
            self.window_surface.blit(self.background_surface, (0, 0))

            # Debug crap
            # chunk = self.test_slider.right_button.drawable_shape.text_box_layout.layout_rows[0].items[0]
            # pygame.draw.line(self.test_slider.right_button.image,
            #                  pygame.Color('#FFFFFF'),
            #                  self.test_slider.right_button.drawable_shape.text_box_layout.layout_rows[0].midleft,
            #                  self.test_slider.right_button.drawable_shape.text_box_layout.layout_rows[0].midright,#chunk.centering_rect,
            #                  1)

            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()
            
        
            

if __name__ == '__main__':
    app = OptionsUIApp()
    app.run()