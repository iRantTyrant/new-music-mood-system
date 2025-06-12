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

const dropdown = document.getElementById("song-select");
const songDetails = document.getElementById("song-details");

dropdown.addEventListener("change", async () => {
  const selectedSong = dropdown.value;

  // Fade out
  songDetails.style.opacity = 0;

  await new Promise(resolve => setTimeout(resolve, 700));

  await loadSongDetails(selectedSong);

  changeDetailsColour(document.getElementById("mood").innerText);

  // Fade in
  setTimeout(() => {
    songDetails.style.opacity = 1;
  }, 50);
});

function changeDetailsColour(mood) {
  const moodColours = {
    "Pleasant": "#FFD700",
    "Happy": "#FFDB58",
    "Aroused": "#FF4500",
    "Angry": "#FF0000",
    "Frustrated": "#C71585",
    "Sad": "#1E90FF",
    "Depressed": "#00008B",
    "Slightly Sad": "#4682B4",
    "Calm": "#00CED1",
    "Relaxed": "#008080",
    "Content": "#006400",
    "Sorrowful": "#4B0082",
    "Neutral / Ambiguous": "#C0C0C0"
  };

  const color = moodColours[mood] || "#000000";

  const ids = ["song-title", "mood", "valence", "arousal", "plot-text", "animation-text"];
  ids.forEach(id => {
    const element = document.getElementById(id);
    if (element) {
      element.style.color = color;
    }
  });

  const glow = document.getElementById("bleed-div");
  if (glow) {
    glow.style.backgroundColor = color;
    glow.style.opacity = "1";
  }

  

}

