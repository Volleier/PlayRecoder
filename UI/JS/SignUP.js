document.getElementById("apiForm").addEventListener("submit", function (event) {
  event.preventDefault();

  const apiKey = document.getElementById("api_key").value;
  const userId = document.getElementById("user_id").value;

  console.log(`Sending data: api_key=${apiKey}&user_id=${userId}`);

  fetch("/save", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `api_key=${apiKey}&user_id=${userId}`,
  })
    .then((response) =>
      response.json().then((data) => ({ status: response.status, body: data }))
    )
    .then(({ status, body }) => {
      if (status === 200) {
        window.location.href = body.redirect;
      } else {
        alert(body.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
