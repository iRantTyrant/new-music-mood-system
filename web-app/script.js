//Get the list of the songs(directories)
async function loadSongs() {
  //MAke an http call to the api to return the jsonfied names of the directories
  const res = await fetch("/list_songs");
  const songs = await res.json();

  //For each of the names add them to the select dropdown as an option
  const select = document.getElementById("song-select");
  songs.forEach(song => {
    const option = document.createElement("option");
    option.value = song;
    option.innerText = song;
    select.appendChild(option);
  });
}

//Update the details function
async function loadSongDetails(song) {
  //Make an http call to the api and fetch the details of the song 
  const metaRes = await fetch(`/output/${song}/metadata.json`);
  const meta = await metaRes.json();

  //Update the details in their corresponding element
  document.getElementById("song-title").innerText = meta.title;
  document.getElementById("mood").innerText = meta.mood;
  document.getElementById("valence").innerText = meta.valence.toFixed(2);
  document.getElementById("arousal").innerText = meta.arousal.toFixed(2);

  //Update the plot and video using the src attribute to fetch through an http  request the corresponding plot
  document.getElementById("plot").src = `/output/${song}/mood_plot.png`;
  document.getElementById("animation").src = `/output/${song}/mood_animation.mp4`;

  //Remove hidden so it shows up
  document.getElementById("song-details").classList.remove("hidden");
}

//Load all songs to the list 
loadSongs();

//Call to the api through a fetch to get the .wav file in each song directory and send it as a src to the audio element
async function loadAudio(song){
  
  const metaAudio = await fetch(`/output/${song}/list_files`);
  const wavFiles = await metaAudio.json(); 
  
  if (wavFiles.length>0){
  const wavFile = wavFiles[0];
  const audioPlayer = document.getElementById("audio-player")
  audioPlayer.src = `/output/${song}/${wavFile}`;
  audioPlayer.load();
  
  try{
    await audioPlayer.play();
  }catch (err){
   
  }

  } 
}

const dropdown = document.getElementById("song-select");
const songDetails = document.getElementById("song-details");

//Animation for the fade in fade out for when we cahnge songs
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

  //Load song
  loadAudio(selectedSong);
});


//Functions to change the colour of the details and glow for each mood 
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

