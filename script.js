const fileInput = document.getElementById('fileInput');
const uploadButton = document.getElementById('uploadButton');
const statusElement = document.getElementById('status');
const progressContainer = document.getElementById('progressContainer');
const progressBar = document.getElementById('progressBar');

uploadButton.addEventListener('click', () => {
    const file = fileInput.files[0];

    if (!file) {
        statusElement.textContent = "Please select a PDF file.";
        statusElement.style.color = "red";
        return;
    }

    if (file.type !== 'application/pdf') {
        statusElement.textContent = "Only PDF files are allowed.";
        statusElement.style.color = "red";
        return;
    }

    statusElement.textContent = "Uploading...";
    statusElement.style.color = "orange";
    progressContainer.style.display = 'block';  // Show progress bar

    const formData = new FormData();
    formData.append('pdf', file);

    fetch('/upload', {
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'application/json',
        },
        onUploadProgress: function (progressEvent) {
            if (progressEvent.lengthComputable) {
                const percentComplete = (progressEvent.loaded / progressEvent.total) * 100;
                progressBar.style.width = percentComplete + '%';
            }
        }
    })
    .then(response => response.json())
    .then(data => {
        statusElement.textContent = "Upload Complete!";
        statusElement.style.color = "green";
        progressBar.style.width = '100%';
        // Optionally, display the table data or logs in the UI
        console.log(data); // Assuming the backend sends extracted table data
    })
    .catch(err => {
        statusElement.textContent = "Upload Failed!";
        statusElement.style.color = "red";
        console.error(err);
    });
});