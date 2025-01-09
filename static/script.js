let videoElement = document.getElementById('parking-video');
let startBtn = document.getElementById('startBtn');
let stopBtn = document.getElementById('stopBtn');

startBtn.addEventListener('click', function() {
    // Enable video stream and buttons
    videoElement.src = "/video_feed";
    startBtn.disabled = true;
    stopBtn.disabled = false;
});

stopBtn.addEventListener('click', function() {
    // Stop video stream
    videoElement.src = "";
    startBtn.disabled = false;
    stopBtn.disabled = true;
});
