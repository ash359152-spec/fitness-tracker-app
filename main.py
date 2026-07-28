from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp


class FitnessTrackerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(16), spacing=dp(12), **kwargs)

        self.workouts = []

        # Title
        self.add_widget(Label(
            text="Fitness Tracker",
            font_size=dp(28),
            size_hint=(1, 0.1)
        ))

        # Summary row
        self.summary_label = Label(
            text="Total workouts logged: 0",
            font_size=dp(16),
            size_hint=(1, 0.08)
        )
        self.add_widget(self.summary_label)

        # Input row: exercise name
        input_row1 = BoxLayout(orientation="horizontal", size_hint=(1, 0.08), spacing=dp(8))
        input_row1.add_widget(Label(text="Exercise:", size_hint=(0.3, 1)))
        self.exercise_input = TextInput(multiline=False, size_hint=(0.7, 1))
        input_row1.add_widget(self.exercise_input)
        self.add_widget(input_row1)

        # Input row: duration (minutes)
        input_row2 = BoxLayout(orientation="horizontal", size_hint=(1, 0.08), spacing=dp(8))
        input_row2.add_widget(Label(text="Minutes:", size_hint=(0.3, 1)))
        self.duration_input = TextInput(multiline=False, input_filter="int", size_hint=(0.7, 1))
        input_row2.add_widget(self.duration_input)
        self.add_widget(input_row2)

        # Log button
        log_button = Button(
            text="Log Workout",
            size_hint=(1, 0.1),
            on_press=self.log_workout
        )
        self.add_widget(log_button)

        # Scrollable list of logged workouts
        self.history_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(6))
        self.history_layout.bind(minimum_height=self.history_layout.setter("height"))

        scroll = ScrollView(size_hint=(1, 0.56))
        scroll.add_widget(self.history_layout)
        self.add_widget(scroll)

    def log_workout(self, instance):
        exercise = self.exercise_input.text.strip()
        duration = self.duration_input.text.strip()

        if not exercise or not duration:
            return  # ignore incomplete entries

        entry = f"{exercise} — {duration} min"
        self.workouts.append(entry)

        entry_label = Label(
            text=entry,
            size_hint_y=None,
            height=dp(30),
            font_size=dp(14)
        )
        self.history_layout.add_widget(entry_label)

        self.summary_label.text = f"Total workouts logged: {len(self.workouts)}"

        # Clear inputs for the next entry
        self.exercise_input.text = ""
        self.duration_input.text = ""


class FitnessTrackerApp(App):
    def build(self):
        return FitnessTrackerLayout()


if __name__ == "__main__":
    FitnessTrackerApp().run()
