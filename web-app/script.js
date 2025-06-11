async function loadSongs() {
    const res = await fetch("/list_songs");
    const songs = await res.json();

    const select = document.getElementById("song-select");
    songs.forEach(song => {
    const option = document.createElement("option");
    option.value = song;
    option.innerText = song;
    select.appendChild(option);
    });
}

async function loadSongDetails(song) {
    const metaRes = await fetch(`/output/${song}/metadata.json`);
    const meta = await metaRes.json();

    document.getElementById("song-title").innerText = meta.title;
    document.getElementById("mood").innerText = meta.mood;
    document.getElementById("valence").innerText = meta.valence.toFixed(2);
    document.getElementById("arousal").innerText = meta.arousal.toFixed(2);

    document.getElementById("plot").src = `/output/${song}/mood_plot.png`;
    document.getElementById("animation").src = `/output/${song}/mood_animation.mp4`;

    document.getElementById("song-details").classList.remove("hidden");
}

loadSongs();
 
document.addEventListener("DOMContentLoaded", () => {
    const dropdown = document.getElementById("song-select");
    const plotImg = document.getElementById("plot");
    const animationVideo = document.getElementById("animation");
    const container = document.getElementById("visualization-container");

    async function fadeOutThenChange(song) {
        // Add fade-out
        container.classList.add("opacity-0");

        // Wait for the fade-out to complete (based on Tailwind duration-500)
        await new Promise((resolve) => setTimeout(resolve, 500));

        // Clear previous sources explicitly
        animationVideo.pause();
        animationVideo.removeAttribute("src");
        animationVideo.load(); // reset video

        // Bust cache with timestamp
        const cacheBuster = `?v=${Date.now()}`;
        const newImgSrc = `/output/${song}/mood_plot.png${cacheBuster}`;
        const newVideoSrc = `/output/${song}/mood_animation.mp4${cacheBuster}`;

        // Replace sources
        plotImg.src = newImgSrc;
        animationVideo.src = newVideoSrc;

        // Wait for image load
        await new Promise((resolve) => {
            plotImg.onload = () => resolve();
        });

        // Wait for video to be able to play (not just loaded)
        await new Promise((resolve) => {
            animationVideo.oncanplay = () => resolve();
        });

        // Small delay for safety
        await new Promise((resolve) => setTimeout(resolve, 100));

        // Fade-in
        container.classList.remove("opacity-0");
        animationVideo.play(); // play after fully loaded
    }

    dropdown.addEventListener("change", (e) => {
        const song = e.target.value;
        fadeOutThenChange(song);
    });
});
