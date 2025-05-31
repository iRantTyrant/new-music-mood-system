import matplotlib.pyplot as plt
import os

_points = []       # Για τα σημεία κάθε τραγουδιού (dynamic)
_mean_points = []  # Για τα mean σημεία όλων των τραγουδιών (all songs plot)

mood_colors = {
    "Neutral / Ambiguous": "gray",
    "Happy": "yellow",
    "Relaxed": "green",
    "Calm": "blue",
    "Angry": "red",
    "Sad": "purple",
    "Depressed": "brown",
    "Pleasant": "#FFD700",
    "Aroused": "#FF4500",
    "Frustrated": "#8B0000",
    "Slightly Sad": "#000000",
    "Content": "#90EE90",
    "Sorrowful": "#4B0082"
}

def add_point_to_visualization(valence, arousal, mood):
    global _points
    _points.append((valence, arousal, mood))

def add_mean_point(valence, arousal, mood):
    global _mean_points
    _mean_points.append((valence, arousal, mood))

def reset_points():
    global _points
    _points.clear()

def reset_mean_points():
    global _mean_points
    _mean_points.clear()

def plot_all_points(audio_file_name , output_dir="plots"):
    if not _points:
        print("No data to plot.")
        return

    plt.figure(figsize=(8, 8))
    ax = plt.gca()
    ax.set_facecolor('#f9f9f9')

    os.makedirs(output_dir, exist_ok=True)

    neutral_zone = plt.Circle((0, 0), 0.05, color='gray', alpha=0.2, label="Neutral zone")
    ax.add_artist(neutral_zone)

    for valence, arousal, mood in _points:
        color = mood_colors.get(mood, "black")
        ax.scatter(valence, arousal, color=color, s=20, alpha=0.7, label=mood)

    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.xlabel("Valence (-1 to 1)")
    plt.ylabel("Arousal (-1 to 1)")
    plt.title(f"Valence-Arousal Mood Map for {audio_file_name}")

    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    plt.legend(unique.values(), unique.keys(), loc="upper right", fontsize='small')

    plt.grid(True, linestyle=':', linewidth=0.5)
    plt.tight_layout()
    output_path = os.path.join(output_dir, f"{audio_file_name}_mood_plot.png")
    plt.savefig(output_path)
    plt.close()
    print(f"[INFO] Saved mood plot: {output_path}")

def plot_all_mean_points():
    if not _mean_points:
        print("No mean data to plot.")
        return

    plt.figure(figsize=(8, 8))
    ax = plt.gca()
    ax.set_facecolor('#f9f9f9')

    os.makedirs("plots", exist_ok=True)

    neutral_zone = plt.Circle((0, 0), 0.05, color='gray', alpha=0.2, label="Neutral zone")
    ax.add_artist(neutral_zone)

    for valence, arousal, mood in _mean_points:
        color = mood_colors.get(mood, "black")
        ax.scatter(valence, arousal, color=color, s=50, alpha=0.9, label=mood)  # Μεγαλύτερα σημεία

    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.xlabel("Valence (-1 to 1)")
    plt.ylabel("Arousal (-1 to 1)")
    plt.title("Mean Valence-Arousal Mood Map for All Songs")

    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    plt.legend(unique.values(), unique.keys(), loc="upper right", fontsize='small')

    plt.grid(True, linestyle=':', linewidth=0.5)
    plt.tight_layout()
    output_path = "plots/all_songs_mean_mood_plot.png"
    plt.savefig(output_path)
    plt.close()
    print(f"[INFO] Saved mean mood plot for all songs: {output_path}")

