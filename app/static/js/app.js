document.querySelector(".logout-btn").addEventListener("click", async () => {
  window.location.href = "/login";
  await fetch("/api/auth/logout", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });
});
