import sys
# Create a crash-log text file on your phone if the app fails to boot
sys.stderr = open('curtsy_crash_log.txt', 'w')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
from datetime import datetime
import random
import json
import os
from plyer import notification

class Curtsy(App):
    def build(self):
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
        except Exception as e:
            print(f"Data loading error caught: {e}")

        if platform == 'android':
            try:
                self.request_android_permissions()
            except Exception as e:
                print(f"Permissions hook failed: {e}")

        # Standard heartbeat timer
        Clock.schedule_interval(self.check_time_loop, 30)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text='🌟 Curtsy', font_size=28, bold=True))

        layout.add_widget(Label(text='Notification Time (HH:MM):', font_size=16))
        self.time_input = TextInput(text=self.daily_time, multiline=False, font_size=18)
        layout.add_widget(self.time_input)

        layout.add_widget(Label(text='Your Tasks (one per line):', font_size=16))
        self.task_input = TextInput(text='\n'.join(self.tasks), multiline=True, font_size=16)
        layout.add_widget(self.task_input)

        btn_save = Button(text='Save Tasks & Time', size_hint=(1, 0.15), font_size=18)
        btn_save.bind(on_press=self.save_data)
        layout.add_widget(btn_save)

        btn_test = Button(text='Send Test Notification', size_hint=(1, 0.15), font_size=18)
        btn_test.bind(on_press=self.send_test)
        layout.add_widget(btn_test)

        return layout

    def check_time_loop(self, dt):
        now = datetime.now()
        current_time_str = now.strftime("%H:%M")
        current_day = now.date()

        if current_day != self.last_checked_day:
            self.notification_sent_today = False
            self.last_checked_day = current_day

        if current_time_str == self.daily_time and not self.notification_sent_today:
            self.notification_sent_today = True  
            self.fire_scheduled_notification()

    def fire_scheduled_notification(self):
        if self.tasks:
            task = random.choice(self.tasks)
            try:
                notification.notify(
                    title="🌅 Daily Task Reminder",
                    message=task,
                    timeout=10
                )
            except Exception as e:
                print(f"Scheduled notification failed: {e}")

    def request_android_permissions(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.POST_NOTIFICATIONS])
        except Exception as e:
            print(f"Permission Request failed: {e}")

    def load_data(self):
        if os.path.exists('daily_tasks.json'):
            try:
                with open('daily_tasks.json', 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get('tasks', self.tasks)
                    self.daily_time = data.get('time', self.daily_time)
            except:
                pass

    def save_data(self, instance):
        tasks_str = self.task_input.text.strip()
        self.tasks = [t.strip() for t in tasks_str.split('\n') if t.strip()]
        
        raw_time = self.time_input.text.strip()
        if len(raw_time) == 4 and ":" in raw_time:
            raw_time = "0" + raw_time 
        self.daily_time = raw_time

        data = {"tasks": self.tasks, "time": self.daily_time}
        with open('daily_tasks.json', 'w') as f:
            json.dump(data, f)
        
        self.notification_sent_today = False
        print(f"✅ Saved! Tasks: {len(self.tasks)} | Time: {self.daily_time}")

    def send_test(self, instance):
        if self.tasks:
            task = random.choice(self.tasks)
            try:
                notification.notify(
                    title="🌟 Your Daily New Task",
                    message=task,
                    timeout=10
                )
            except Exception as e:
                print(f"Notification display failed: {e}")

if __name__ == '__main__':
    try:
        Curtsy().run()
    except Exception as e:
        import traceback
        with open('curtsy_boot_crash.txt', 'w') as f:
            traceback.print_exc(file=f)
