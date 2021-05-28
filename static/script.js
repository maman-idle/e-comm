function buy() {
  const buy = document.querySelector(".buy_opt");

  if (buy.classList.contains("hide")) {
    buy.classList.remove("hide");
  } else {
    buy.classList.add("hide");
  }
}
