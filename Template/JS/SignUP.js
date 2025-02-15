document.getElementById('apiForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const apiKey = document.getElementById('api_key').value;
    const userId = document.getElementById('user_id').value;

    fetch('/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `api_key=${apiKey}&user_id=${userId}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            if (response.ok) {
                window.location.href = '/games';
            }
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});