document.addEventListener('DOMContentLoaded', () => {
    const inputElement = document.getElementById('fileInput');
    const poseImage = document.getElementById('poseImage');

    inputElement.addEventListener('change', (e) => {
        const file = e.target.files[0];

        if (file) {
            // Create a FormData object to send the file
            const formData = new FormData();
            formData.append('photo', file);

            // Make an AJAX POST request to the server to send the file
            fetch('/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    // Handle the received pose data
                    const resultImage = data.result;
                    // Display the received pose image in the <img> element
                    poseImage.src = 'data:image/jpeg;base64,' + resultImage;
                })
                .catch(error => {
                    console.error('Error uploading file:', error);
                });
        }
    });
});