document.addEventListener("DOMContentLoaded", () => {
  const flash = document.querySelector(".flash");
  if (flash) {
    setTimeout(() => {
      flash.style.opacity = "0";
      setTimeout(() => flash.remove(), 1000);
    }, 3500);
  }

  const hoje = new Date().toISOString().split("T")[0];
  const campoData = document.querySelector("#data");
  if (campoData) campoData.min = hoje;
});
