import sys
sys.stderr = open('curtsy_crash_log.txt', 'w')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.utils import platform
from kivy.graphics import Color, RoundedRectangle
from datetime import datetime
import random
import json
import os
from plyer import notification

# --- REUSABLE CUSTOM CARD BACKDROP ---
class MaterialCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        with self.canvas.before:
            Color(1, 1, 1, 0.06) # Translucent overlay style card
            self.rect = RoundedRectangle(radius=[15])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# --- SCREEN 1: THE MAIN HOME INTERFACE ---
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=25, spacing=15)
        
        # Initialize background canvas object link
        with self.layout.canvas.before:
            self.bg_color = Color(0, 0, 0, 1) # Fallback baseline color
            self.bg_rect = RoundedRectangle()
        self.layout.bind(pos=self.update_bg, size=self.update_bg)

        # App Branding Header
        header = BoxLayout(size_hint_y=0.1)
        header.add_widget(Label(text='🌟 Curtsy', font_size=28, bold=True, halign='left'))
        
        btn_settings = Button(text='⚙️ Settings', size_hint_x=0.3, font_size=16, background_color=(1, 1, 1, 0.15))
        btn_settings.bind(on_press=self.go_to_settings)
        header.add_widget(btn_settings)
        self.layout.add_widget(header)

        # Main Task Focus Display Card
        self.card = MaterialCard(size_hint_y=0.4)
        self.card.add_widget(Label(text="TODAY'S HIGHLIGHT", font_size=14, bold=True, color=(0.7, 0.7, 0.8, 1)))
        
        self.task_display = Label(
            text="Tap below to reveal your first task!", 
            font_size=20, 
            text_size=(400, None), 
            halign='center', 
            valign='middle'
        )
        self.card.add_widget(self.task_display)
        self.layout.add_widget(self.card)

        # Action Buttons Layout
        self.layout.add_widget(Label(size_hint_y=0.05)) # Spacer
        
        btn_roll = Button(text='🎲 Roll New Daily Task', size_hint_y=0.15, font_size=18, bold=True, background_color=(0.2, 0.6, 0.4, 1))
        btn_roll.bind(on_press=self.roll_new_task)
        self.layout.add_widget(btn_roll)

        btn_test = Button(text='🔔 Send Test Notification', size_hint_y=0.12, font_size=16, background_color=(0.3, 0.5, 0.8, 1))
        btn_test.bind(on_press=self.send_notification)
        self.layout.add_widget(btn_test)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        """Forces canvas color to redraw with the user's active preset choice on view entry"""
        app = App.get_running_app()
        chosen_rgb = app.bg_presets[app.active_bg_name]
        self.bg_color.rgb = chosen_rgb

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def go_to_settings(self, instance):
        self.manager.current = 'settings'

    def roll_new_task(self, instance):
        app = App.get_running_app()
        if app.tasks:
            self.task_display.text = random.choice(app.tasks)

    def send_notification(self, instance):
        App.get_running_app().send_test(None)

# --- SCREEN 2: THE USER SETTINGS PANEL ---
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=25, spacing=10)

        with self.layout.canvas.before:
            self.bg_color = Color(0, 0, 0, 1)
            self.bg_rect = RoundedRectangle()
        self.layout.bind(pos=self.update_bg, size=self.update_bg)

        # Header Title
        self.layout.add_widget(Label(text='⚙️ Configuration Panel', font_size=24, bold=True, size_hint_y=0.06))

        # Time Management Section
        self.layout.add_widget(Label(text='Daily Alert Time (HH:MM Format):', font_size=14, size_hint_y=0.04, halign='left'))
        self.time_input = TextInput(text='', multiline=False, font_size=16, size_hint_y=0.06, background_color=(0.18, 0.18, 0.22, 1), foreground_color=(1,1,1,1))
        self.layout.add_widget(self.time_input)

        # Task Management Section
        self.layout.add_widget(Label(text='Customize Task Pool (One choice per line):', font_size=14, size_hint_y=0.04, halign='left'))
        self.task_input = TextInput(text='', multiline=True, font_size=14, size_hint_y=0.35, background_color=(0.18, 0.18, 0.22, 1), foreground_color=(1,1,1,1))
        self.layout.add_widget(self.task_input)

        # NEW BACKGROUND PICKER INTERFACE BLOCK
        self.layout.add_widget(Label(text='Select Application Background Theme:', font_size=14, size_hint_y=0.04, halign='left'))
        picker_tray = BoxLayout(spacing=8, size_hint_y=0.1)
        
        # We loop through the app presets structure to dynamically generate theme layout options
        app = App.get_running_app()
        for theme_name in ['Midnight', 'Forest', 'Ocean', 'Burgundy', 'Obsidian']:
            btn_theme = Button(
                text=theme_name, 
                font_size=12,
                background_normal='',
                background_color=list(app.bg_presets[theme_name]) + [1]
            )
            # Use an explicit lambda structure to bind the correct name tracking key natively
            btn_theme.bind(on_press=lambda inst, name=theme_name: self.change_preview_theme(name))
            picker_tray.add_widget(btn_theme)
        self.layout.add_widget(picker_tray)

        # Bottom Button Tray
        button_tray = BoxLayout(spacing=15, size_hint_y=0.12)
        
        btn_back = Button(text='Cancel', font_size=16, background_color=(0.5, 0.2, 0.2, 1))
        btn_back.bind(on_press=self.cancel_settings)
        button_tray.add_widget(btn_back)

        btn_save = Button(text='Save Changes', font_size=16, bold=True, background_color=(0.2, 0.6, 0.4, 1))
        btn_save.bind(on_press=self.save_settings)
        button_tray.add_widget(btn_save)
        
        self.layout.add_widget(button_tray)
        self.add_widget(self.layout)

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def on_pre_enter(self):
        """Loads values and handles active canvas colors prior to drawing panel layout"""
        app = App.get_running_app()
        self.time_input.text = app.daily_time
        self.task_input.text = '\n'.join(app.tasks)
        self.bg_color.rgb = app.bg_presets[app.active_bg_name]
        self.temp_selected_bg = app.active_bg_name

    def change_preview_theme(self, name):
        """Updates color matrix values instantly on screen canvas to provide immediate visual feedback"""
        app = App.get_running_app()
        self.bg_color.rgb = app.bg_presets[name]
        self.temp_selected_bg = name

    def cancel_settings(self, instance):
        self.manager.current = 'main'

    def save_settings(self, instance):
        app = App.get_running_app()
        
        # Save time input changes
        raw_time = self.time_input.text.strip()
        if len(raw_time) == 4 and ":" in raw_time:
            raw_time = "0" + raw_time 
        app.daily_time = raw_time

        # Save task pool inputs
        tasks_str = self.task_input.text.strip()
        app.tasks = [t.strip() for t in tasks_str.split('\n') if t.strip()]
        
        # Permanently assign the preview background theme flag to global state
        app.active_bg_name = self.temp_selected_bg

        # Write all parameters natively to persistence file module layout
        data = {
            "tasks": app.tasks, 
            "time": app.daily_time,
            "background": app.active_bg_name
        }
        with open('daily_tasks.json', 'w') as f:
            json.dump(data, f)
        
        app.notification_sent_today = False 
        self.manager.current = 'main'

# --- MAIN APPLICATION CORE RUNNER LOOP ---
class Curtsy(App):
    def build(self):
        # 5 Premium Dark-Mode RGB Floating Point Presets
        self.bg_presets = {
            'Midnight': (0.08, 0.08, 0.12),   # Deep slate navy blue
            'Forest':   (0.06, 0.10, 0.08),   # Muted spruce green
            'Ocean':    (0.04, 0.09, 0.11),   # Dark deep teal marine
            'Burgundy': (0.12, 0.06, 0.07),   # Rich velvety dark wine red
            'Obsidian': (0.05, 0.05, 0.05)    # Clean minimalist monochromatic dark gray
        }
        self.active_bg_name = 'Midnight' # System fallback baseline choice
        
        self.tasks = [
            "Go for a 30-minute walk outdoors.",
            "Drink 2 liters of water today.",
            "Read 10 pages of a book.",
            "Clean one small area of your home.",
            "Practice 5 minutes of meditation.",
            "Learn one new vocabulary word.",
            "Call or message a friend or family member.",
            "Try a new healthy recipe.",
        ]
        self.daily_time = "08:00"
        self.notification_sent_today = False  
        self.last_checked_day = datetime.now().date()
        
        try:
            self.load_data()
        except:
            pass

        if platform == 'android':
            try:
                self.request_android_permissions()
            except:
                pass

        Clock.schedule_interval(self.check_time_loop, 30)

        sm = ScreenManager()
 def load_data(self):
        if os.path.exists('daily_tasks.json'):
            try:
                with open('daily_tasks.json', 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', self.tasks)
                    self.daily_time = data.get('time', self.daily_time)
                    self.active_bg_name = data.get('background', self.active_bg_name)
            except:
                pass

    def send_test(self, instance):
        if self.tasks:
            task = random.choice(self.tasks)
            try:
                notification.notify(
                    title="🌟 Your Daily New Task",
                    message=task,
                    timeout=10
                )
            except:
                pass

if __name__ == '__main__':
    try:
        Curtsy().run()
    except Exception as e:
        import traceback
        with open('curtsy_boot_crash.txt', 'w') as f:
            traceback.print_exc(file=f)
