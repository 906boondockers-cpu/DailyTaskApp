from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
from datetime import datetime  # Added to read system time
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
        self.notification_sent_today = False  # Track to prevent spamming within the same minute
        self.last_checked_day = datetime.now().date()
        
        self.load_data()

        if platform == 'android':
            self.request_android_permissions()

        # Start the background timer loop to check the clock every 30 seconds
        Clock.schedule_interval(self.check_time_loop, 30)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text='🌟 Daily New Task App', font_size=28, bold=True))

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
        """Runs silently every 30 seconds to check if it's time to fire a task notification"""
        now = datetime.now()
        current_time_str = now.strftime("%H:%M")
        current_day = now.date()

        # Reset the daily anti-spam lock when the calendar date rolls over
        if current_day != self.last_checked_day:
            self.notification_sent_today = False
            self.last_checked_day = current_day

        # Trigger if the clock matches the target time and we haven't sent one yet today
        if current_time_str == self.daily_time and not self.notification_sent_today:
            self.notification_sent_today = True  # Lock it out for this minute
            self.fire_scheduled_notification()

    def fire_scheduled_notification(self):
        """Selects a random item and pushes it to the system tray"""
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
        
        # Keep formatting uniform (clean up user whitespace padding)
        raw_time = self.time_input.text.strip()
        if len(raw_time) == 4 and ":" in raw_time:
            raw_time = "0" + raw_time # Auto fix H:MM to HH:MM
        self.daily_time = raw_time

        data = {"tasks": self.tasks, "time": self.daily_time}
        with open('daily_tasks.json', 'w') as f:
            json.dump(data, f)
        
        # Reset tracker when time is updated so user can test immediate new times
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
    curtsy().run()
