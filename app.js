// Replace with the API Gateway endpoint output from CloudFormation
const API_URL = "https://********.execute-api.us-east-1.amazonaws.com/status";

const btn = document.getElementById("callApiBtn");
const loader = document.getElementById("loader");
const result = document.getElementById("result");
const errorDiv = document.getElementById("error");

btn.addEventListener("click", async () => {
  loader.classList.remove("hidden");
  result.classList.add("hidden");
  errorDiv.classList.add("hidden");

  try {
    const response = await fetch(API_URL);
    if (!response.ok) {
      throw new Error("Backend error");
    }

    const data = await response.json();

    document.getElementById("status").innerText = data.status;
    document.getElementById("message").innerText = data.message;
    document.getElementById("time").innerText = data.server_time;
    document.getElementById("requestId").innerText = data.request_id;
    document.getElementById("random").innerText = data.random_value;
    document.getElementById("count").innerText = data.request_count;

    result.classList.remove("hidden");
  } catch (err) {
    errorDiv.innerText = "Failed to reach backend!";
    errorDiv.classList.remove("hidden");
  } finally {
    loader.classList.add("hidden");
  }
});
