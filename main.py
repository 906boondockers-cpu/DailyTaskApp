from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
import random
import json
import os
from plyer import notification

class DailyTaskApp(App):
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
        self.load_data()

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
        self.daily_time = self.time_input.text.strip()

        data = {"tasks": self.tasks, "time": self.daily_time}
        with open('daily_tasks.json', 'w') as f:
            json.dump(data, f)
        
        print(f"✅ Saved! Tasks: {len(self.tasks)} | Time: {self.daily_time}")

    def send_test(self, instance):
        if self.tasks:
            task = random.choice(self.tasks)
            notification.notify(
                title="🌟 Your Daily New Task",
                message=task,
                timeout=10
            )

if __name__ == '__main__':
    DailyTaskApp().run()