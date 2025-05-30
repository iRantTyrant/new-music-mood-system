import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from matplotlib.animation import FFMpegWriter
from src.visualization import mood_colors, _points
from tqdm import tqdm
import os

def create_dynamic_video(audio_file_name, frame_interval_sec=0.5):
    points = _points
    if not points:
        print(f"[VIDEO] No points found for {audio_file_name}. Skipping.")
        return

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor('#f9f9f9')
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.xlabel("Valence (-1 to 1)")
    plt.ylabel("Arousal (-1 to 1)")
    plt.title(f"Dynamic Mood Map - {audio_file_name}")
    plt.grid(True, linestyle=':', linewidth=0.5)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.add_artist(Circle((0, 0), 0.05, color='gray', alpha=0.2))

    # Legend
    for mood, color in mood_colors.items():
        ax.scatter([], [], color=color, label=mood)
    ax.legend(loc="upper right", fontsize='small')

    line, = ax.plot([], [], color='red', linewidth=2)
    trail_length = 5
    trail_points = []
    all_dots = []

    def init():
        return [line] + all_dots

    def update(frame):
        val, ar, mood = points[frame]
        trail_points.append((val, ar))
        if len(trail_points) > trail_length:
            trail_points.pop(0)
        x_trail, y_trail = zip(*trail_points)
        color = mood_colors.get(mood, "black")
        line.set_data(x_trail, y_trail)
        line.set_color(color)

        dot = ax.scatter(val, ar, color=color, s=30, alpha=0.8)
        all_dots.append(dot)
        ax.set_title(f"Dynamic Mood Map - {audio_file_name}\nTime: {frame * frame_interval_sec:.1f}s")
        return [line] + all_dots

    anim = animation.FuncAnimation(
        fig, update, init_func=init,
        frames=tqdm(range(len(points)), desc=f"Rendering {audio_file_name}"),
        interval=frame_interval_sec * 1000,
        blit=False, repeat=False
    )

    output_path = f"plots/{audio_file_name}_mood_animation.mp4"
    os.makedirs("plots", exist_ok=True)
    print(f"[VIDEO] Saving animation to: {output_path}")
    anim.save(output_path, writer=FFMpegWriter(fps=int(1/frame_interval_sec)))
    plt.close()
    print(f"[VIDEO] Saved successfully: {output_path}")


