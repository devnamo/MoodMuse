import json
import random
from datetime import datetime
import os
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

# Setup Rich console
console = Console()

# Mood styles (accessible + white-friendly backgrounds)
mood_styles = {
    "happy": {
        "color": "yellow",
        "emoji": "🌞",
        "header": "☁️ MoodMuse says... Shine on! ☁️"
    },
    "anxious": {
        "color": "sky_blue3",
        "emoji": "💙",
        "header": "🕊️ Breathe. You're safe here. 💙"
    },
    "tired": {
        "color": "medium_purple3",
        "emoji": "😴",
        "header": "☁️ Slow down and rest, love ☁️"
    },
    "motivated": {
        "color": "green",
        "emoji": "🚀",
        "header": "✨ You’ve got this, go girlieee! ✨"
    },
    "sad": {
        "color": "medium_purple3",
        "emoji": "😞",
        "header": "🌧️ It's okay to feel. I'm here. 💗"
    },
    "grateful": {
        "color": "dark_orange3",
        "emoji": "🌻",
        "header": "💛 Gratitude unlocks joy 💛"
    }
}

# Load mood data
try:
    with open("mood_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    console.print("[red]❌ mood_data.json not found![/red]")
    exit()

# 🌸 MoodMuse Header
console.print("\n[bold magenta] 🧚‍♀️🌸 Welcome to MoodMuse 🌸🧚‍♀️[/bold magenta]", justify="center")
console.print("[dim] a little light for your mood\n[/dim]", justify="center")

# Display moods with emoji
console.print("How are you feeling today?\n", style="italic")
moods = list(data.keys())
for i, mood in enumerate(moods, 1):
    emoji = mood_styles[mood]["emoji"]
    console.print(f"{i}. {mood.capitalize()} {emoji}", style=mood_styles[mood]["color"])

# Mood input
try:
    choice = int(input(f"\n Choose your mood (1-{len(moods)}): "))
    selected_mood = moods[choice - 1]
except (ValueError, IndexError):
    console.print("\n[red]❌ Invalid choice. Please run again.[/red]")
    exit()

# Pull mood data
style = mood_styles[selected_mood]
affirmation = random.choice(data[selected_mood]["affirmations"])
prompt = random.choice(data[selected_mood]["prompts"])

# Header Panel
header_panel = Panel(
    Align.center(style["header"], vertical="middle"),
    style=f"on {style['color']}",
    padding=(1, 2)
)
console.print(header_panel)

# Affirmation Panel
affirm_panel = Panel(
    Align.center(f"{style['emoji']}  {affirmation}  {style['emoji']}", vertical="middle"),
    title=f"[bold white]Affirmation[/bold white]",
    border_style=style["color"],
    padding=(1, 4),
)
console.print(affirm_panel)

# Prompt Panel (Mindful Moment)
prompt_panel = Panel(
    Align.center(f"📝  {prompt}", vertical="middle"),
    title="[bold white]Mindful Moment[/bold white]",
    border_style="white",
    padding=(1, 4),
)
console.print(prompt_panel)

# User response input
user_response = input("\n✍️ Your thoughts on this: ")

# Save to journal
save = input("\n💾 Save this to your journal? (y/n): ").strip().lower()
if save == 'y':
    os.makedirs("logs", exist_ok=True)
    filename = f"logs/journal_{datetime.today().date()}.txt"
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"\n--- {datetime.now().strftime('%I:%M %p')} ({selected_mood}) ---\n")
        file.write(f"Affirmation     : {affirmation}\n")
        file.write(f"Mindful Moment  : {prompt}\n")
        file.write(f"Your Response   : {user_response}\n")
    console.print(f"✅ Saved to [italic]{filename}[/italic]", style="green")
else:
    console.print("🫶 Got it. Be gentle with yourself today.\n", style="dim")
