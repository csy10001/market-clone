const handleSubmitForm = async (event) => {
  event.preventDefault();
  try {
    const res = await fetch("/items", {
      method: "POST",
      body: new FormData(form),
    });
    const data = await res.json();
    if (data === "200") window.location.pathname = "/";
  } catch (e) {
    console.error(e);
  }
};

const form = document.getElementById("write-form");
form.addEventListener("submit", handleSubmitForm);
