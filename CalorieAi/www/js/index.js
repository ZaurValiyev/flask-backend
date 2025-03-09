document.addEventListener('DOMContentLoaded', function () {
    console.log("App loaded!");

    const fileInput = document.getElementById('imageUpload');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultDiv = document.getElementById('result');

    analyzeBtn.addEventListener('click', function () {
        const file = fileInput.files[0];

        if (!file) {
            resultDiv.innerHTML = "<span style='color:red;'>❌ Please select an image to upload!</span>";
            return;
        }

        resultDiv.innerHTML = "🔄 Uploading... Please wait.";
        analyzeBtn.disabled = true;

        const formData = new FormData();
        formData.append('image', file);

        fetch('https://flask-backend-3jls.onrender.com/analyze', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = `<strong>✅ Calories:</strong> ${data.result}`;
        })
        .catch(error => {
            console.error("Upload error:", error);
            resultDiv.innerHTML = "<span style='color:red;'>❌ Error uploading image. Try again.</span>";
        })
        .finally(() => {
            analyzeBtn.disabled = false;
        });
    });
});
