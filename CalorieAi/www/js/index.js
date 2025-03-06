function analyzeImage() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    if (!file) return alert('Please select an image');

    const formData = new FormData();
    formData.append('image', file);

    fetch('http://192.168.1.4:5000/analyze', {  // Change this to your Flask server's IP
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('result').innerText = `Calories: ${data.result}`;
    })
    .catch(error => console.error('Error:', error));
}
