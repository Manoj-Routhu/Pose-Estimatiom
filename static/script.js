document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('videoElement');
    const canvas = document.getElementById('canvasElement');
    const context = canvas.getContext('2d');
    const poseImage = document.getElementById('poseImage');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
            video.onloadedmetadata = () => {
                // Adjust canvas size to match video dimensions
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;

                video.play();
                animatePoseEstimation();
            };
        })
        .catch((error) => {
            console.error('Error accessing the camera:', error);
        });

    function animatePoseEstimation() {
        // Draw the current video frame on the canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert canvas image to base64 data
        const frameData = canvas.toDataURL('image/jpeg');

        // Make an AJAX POST request to the server to send frame data and get pose data
        fetch('/process', {
                method: 'POST',
                body: frameData
            })
            .then(response => response.json())
            .then(data => {
                // Handle the received pose data
                const annotatedImage = data.annotated_image;
                // Display the received pose image in the <img> element
                poseImage.src = 'data:image/jpeg;base64,' + annotatedImage;
            })
            .catch(error => {
                console.error('Error fetching pose data:', error);
            })
            .finally(() => {
                // Request next frame animation
                requestAnimationFrame(animatePoseEstimation);
            });
    }
});