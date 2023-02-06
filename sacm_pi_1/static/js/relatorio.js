var modal_05 = document.getElementById("ModalRelatorio");
var btn_05 = document.getElementById("ButtonModalRelatorio");
var span_05 = document.getElementsByClassName("closeModalRelatorio")[0];

btn_05.onclick = function () {
  modal_05.style.display = "flex";
  modal_05.style.alignItems = "center";
  modal_05.style.justifyContent = "center";
};

span_05.onclick = function () {
  modal_05.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == modal_05) {
    modal_05.style.display = "none";
  }
};

console.log("HERE");
