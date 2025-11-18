document.getElementById("regForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const payload = {
    email: form.email.value,
    full_name: form.full_name.value,
    password: form.password.value || null
  };

  const res = await fetch("/api/register", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });

  const pre = document.getElementById("result");
  if (res.ok) {
    pre.textContent = JSON.stringify(await res.json(), null, 2);
  } else {
    const err = await res.json().catch(() => ({}));
    pre.textContent = `Error ${res.status}: ${err.detail || "Unknown"}`;
  }
});
