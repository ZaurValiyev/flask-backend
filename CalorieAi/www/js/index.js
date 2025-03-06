function analyzeImage() {
    const fileInput = document.getElementById('imageUpload');
    const resultDiv = document.getElementById('result');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const file = fileInput.files[0];

    if (!file) {
        resultDiv.innerHTML = "<span style='color:red;'>Please select an image!</span>";
        return;
    }

    resultDiv.innerHTML = "Analyzing... 🔄";
    analyzeBtn.disabled = true; // Disable button while processing

    const formData = new FormData();
    formData.append('image', file);

    fetch('https://flask-backend-3jls.onrender.com/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        resultDiv.innerHTML = `<strong>Calories:</strong> ${data.result}`;
    })
    .catch(error => {
        console.error('Error:', error);
        resultDiv.innerHTML = "<span style='color:red;'>Error analyzing image. Please try again.</span>";
    })
    .finally(() => {
        analyzeBtn.disabled = false; // Enable button again
    });
}
