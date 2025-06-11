import os
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from tqdm import tqdm
from src.visualization import mood_colors, _points
import subprocess
import shutil
def create_dynamic_animation(audio_file_name, output_dir="plots", frame_interval_sec=0.5):
    points = _points
    if not points:
        print(f"[VIDEO] No points found for {audio_file_name}. Skipping.")
        return

    # Δημιουργία φακέλου για frames
    frames_dir = os.path.join(output_dir, "frames_temp")
    os.makedirs(frames_dir, exist_ok=True)

    trail_length = 3
    trail_points = []

    print("[FRAMES] Creating frames...")
    for i, (val, ar, mood) in tqdm(enumerate(points), total=len(points)):
        trail_points.append((val, ar))
        if len(trail_points) > trail_length:
            trail_points.pop(0)

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_facecolor("#f9f9f9")
        ax.set_xlabel("Valence (-1 to 1)")
        ax.set_ylabel("Arousal (-1 to 1)")
        ax.set_title(f"{audio_file_name} - Time: {i * frame_interval_sec:.1f}s")
        ax.grid(True, linestyle=":", linewidth=0.5)
        ax.axhline(0, color="black", linewidth=0.5)
        ax.axvline(0, color="black", linewidth=0.5)
        ax.add_artist(Circle((0, 0), 0.05, color="gray", alpha=0.2))

        # mood legend
        for mood_label, color in mood_colors.items():
            ax.scatter([], [], color=color, label=mood_label)
        ax.legend(loc="upper right", fontsize="small")

        # draw ALL visited points up to now
        for j in range(i + 1):
            x, y, m = points[j]
            color = mood_colors.get(m, "black")
            ax.scatter(x, y, color=color, s=30, alpha=0.8)

        # κόκκινο snake
        if trail_points:
            x_trail, y_trail = zip(*trail_points)
            ax.plot(x_trail, y_trail, color='red', linewidth=2)

        # σημείο για το current mood
        dot_color = mood_colors.get(mood, "black")
        ax.scatter(val, ar, color=dot_color, s=30, alpha=0.8)

        # αποθήκευση frame
        frame_path = os.path.join(frames_dir, f"frame_{i:04d}.png")
        plt.savefig(frame_path)
        plt.close()

    # μονοπάτια εξόδου
    mp4_path = os.path.join(output_dir, f"mood_animation.mp4")
    gif_path = os.path.join(output_dir, f"mood_animation.gif")

    print("[FFMPEG] Δημιουργία MP4...")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", f"{1/frame_interval_sec}",
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", mp4_path
    ])

    print("[FFMPEG] Δημιουργία GIF...")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", f"{1/frame_interval_sec}",
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        gif_path
    ])

    print(f"[DONE] Saved: {mp4_path} and {gif_path}")

    #clean up frames
    shutil.rmtree(frames_dir)
