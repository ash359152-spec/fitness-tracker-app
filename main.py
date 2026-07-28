from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.widget import Widget


# ---- Color palette ----
BG_COLOR = (0.07, 0.08, 0.1, 1)          # near-black navy
CARD_COLOR = (0.12, 0.13, 0.16, 1)       # dark card
ACCENT_COLOR = (0.35, 0.85, 0.55, 1)     # energetic green
ACCENT_DARK = (0.25, 0.65, 0.42, 1)
TEXT_PRIMARY = (0.95, 0.96, 0.97, 1)
TEXT_SECONDARY = (0.6, 0.63, 0.68, 1)
INPUT_BG = (0.16, 0.17, 0.21, 1)


class RoundedBox(Widget):
    """A widget that draws a rounded rectangle behind whatever sits on top of it."""
    def __init__(self, color, radius=dp(14), **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class StyledInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(
            background_color=(0, 0, 0, 0),
            foreground_color=TEXT_PRIMARY,
            cursor_color=ACCENT_COLOR,
            hint_text_color=TEXT_SECONDARY,
            padding=[dp(14), dp(14), dp(14), dp(14)],
            multiline=False,
            **kwargs
        )
        with self.canvas.before:
            Color(*INPUT_BG)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class WorkoutCard(BoxLayout):
    """A single workout entry styled as a rounded card."""
    def __init__(self, exercise, minutes, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, height=dp(56),
                          padding=[dp(14), dp(0)], **kwargs)
        with self.canvas.before:
            Color(*CARD_COLOR)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.add_widget(Label(
            text=exercise,
            font_size=dp(16),
            color=TEXT_PRIMARY,
            bold=True,
            halign="left",
            valign="middle",
            size_hint=(0.65, 1),
            text_size=(None, None),
        ))

        badge_wrap = BoxLayout(size_hint=(0.35, 1), padding=[0, dp(10)])
        badge = RoundedBox(color=ACCENT_DARK, size_hint=(1, 1))
        badge_label = Label(
            text=f"{minutes} min",
            font_size=dp(13),
            color=(1, 1, 1, 1),
            bold=True,
        )
        badge.add_widget(badge_label)
        badge_label.bind(size=badge.setter("size"))
        badge_wrap.add_widget(badge)
        self.add_widget(badge_wrap)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class FitnessTrackerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(20), spacing=dp(14), **kwargs)

        self.workouts = []

        # ---- Header ----
        header = BoxLayout(orientation="vertical", size_hint=(1, None), height=dp(90), spacing=dp(4))
        header.add_widget(Label(
            text="FITNESS TRACKER",
            font_size=dp(26),
            bold=True,
            color=TEXT_PRIMARY,
            size_hint=(1, None),
            height=dp(36),
        ))
        header.add_widget(Label(
            text="Log your workouts and stay consistent",
            font_size=dp(13),
            color=TEXT_SECONDARY,
            size_hint=(1, None),
            height=dp(20),
        ))
        self.add_widget(header)

        # ---- Summary card ----
        summary_wrap = BoxLayout(size_hint=(1, None), height=dp(64))
        summary_box = RoundedBox(color=CARD_COLOR, size_hint=(1, 1))
        self.summary_label = Label(
            text="0 workouts logged",
            font_size=dp(16),
            bold=True,
            color=ACCENT_COLOR,
        )
        summary_box.add_widget(self.summary_label)
        self.summary_label.bind(size=summary_box.setter("size"))
        summary_wrap.add_widget(summary_box)
        self.add_widget(summary_wrap)

        # ---- Exercise input ----
        self.add_widget(Label(
            text="Exercise",
            font_size=dp(13),
            color=TEXT_SECONDARY,
            size_hint=(1, None),
            height=dp(18),
            halign="left",
            text_size=(Window.width - dp(40), None),
        ))
        self.exercise_input = StyledInput(
            hint_text="e.g. Push-ups, Running, Yoga",
            size_hint=(1, None),
            height=dp(52),
        )
        self.add_widget(self.exercise_input)

        # ---- Duration input ----
        self.add_widget(Label(
            text="Duration (minutes)",
            font_size=dp(13),
            color=TEXT_SECONDARY,
            size_hint=(1, None),
            height=dp(18),
            halign="left",
            text_size=(Window.width - dp(40), None),
        ))
        self.duration_input = StyledInput(
            hint_text="e.g. 30",
            input_filter="int",
            size_hint=(1, None),
            height=dp(52),
        )
        self.add_widget(self.duration_input)

        # ---- Log button ----
        log_button_wrap = BoxLayout(size_hint=(1, None), height=dp(56))
        self.log_button = Button(
            text="LOG WORKOUT",
            font_size=dp(15),
            bold=True,
            background_normal="",
            background_color=ACCENT_COLOR,
            color=(0.05, 0.08, 0.06, 1),
            on_press=self.log_workout,
        )
        log_button_wrap.add_widget(self.log_button)
        self.add_widget(log_button_wrap)

        # ---- History label ----
        self.add_widget(Label(
            text="History",
            font_size=dp(14),
            bold=True,
            color=TEXT_PRIMARY,
            size_hint=(1, None),
            height=dp(24),
            halign="left",
            text_size=(Window.width - dp(40), None),
        ))

        # ---- Scrollable workout history ----
        self.history_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(10))
        self.history_layout.bind(minimum_height=self.history_layout.setter("height"))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.history_layout)
        self.add_widget(scroll)

    def log_workout(self, instance):
        exercise = self.exercise_input.text.strip()
        duration = self.duration_input.text.strip()

        if not exercise or not duration:
            return

        self.workouts.append((exercise, duration))

        card = WorkoutCard(exercise, duration)
        self.history_layout.add_widget(card, index=len(self.history_layout.children))

        count = len(self.workouts)
        label = "workout" if count == 1 else "workouts"
        self.summary_label.text = f"{count} {label} logged"

        self.exercise_input.text = ""
        self.duration_input.text = ""


class FitnessTrackerApp(App):
    def build(self):
        Window.clearcolor = BG_COLOR
        return FitnessTrackerLayout()


if __name__ == "__main__":
    FitnessTrackerApp().run()
