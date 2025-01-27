const displayScreen = document.getElementById("display-screen");

const firstRow = document.getElementsByClassName("first-row");
const secondRow = document.getElementsByClassName("second-row");
const thirdRow = document.getElementsByClassName("third-row");
const fourthRow = document.getElementsByClassName("fourth-row");
const fifthRow = document.getElementsByClassName("fifth-row");

for (let i = 0; i < firstRow.length; i++) {
  firstRow[i].onclick = function () {
    if (firstRow[i].value === "AC") {
      displayScreen.value = "";
    } else if (firstRow[i].value === "CE") {
      displayScreen.value = displayScreen.value.toString().slice(0, -1);
    } else if (firstRow[i].value === ".") {
      displayScreen.value += ".";
    } else if (firstRow[i].value === "÷") {
      displayScreen.value += "/";
    }
  };
}

for (let i = 0; i < secondRow.length; i++) {
  secondRow[i].onclick = function () {
    if (secondRow[i].value === "7") {
      displayScreen.value += "7";
    } else if (secondRow[i].value === "8") {
      displayScreen.value += "8";
    } else if (secondRow[i].value === "9") {
      displayScreen.value += "9";
    } else if (secondRow[i].value === "x") {
      displayScreen.value += "*";
    }
  };
}

for (let i = 0; i < thirdRow.length; i++) {
  thirdRow[i].onclick = function () {
    if (thirdRow[i].value === "4") {
      displayScreen.value += "4";
    } else if (thirdRow[i].value === "5") {
      displayScreen.value += "5";
    } else if (thirdRow[i].value === "6") {
      displayScreen.value += "6";
    } else if (thirdRow[i].value === "-") {
      displayScreen.value += "-";
    }
  };
}

for (let i = 0; i < fourthRow.length; i++) {
  fourthRow[i].onclick = function () {
    if (fourthRow[i].value === "1") {
      displayScreen.value += "1";
    } else if (fourthRow[i].value === "2") {
      displayScreen.value += "2";
    } else if (fourthRow[i].value === "3") {
      displayScreen.value += "3";
    } else if (fourthRow[i].value === "+") {
      displayScreen.value += "+";
    }
  };
}

for (let i = 0; i < fifthRow.length; i++) {
  fifthRow[i].onclick = function () {
    if (fifthRow[i].value === "0") {
      displayScreen.value += "0";
    } else if (fifthRow[i].value === "=") {
      displayScreen.value = eval(displayScreen.value);
    }
  };
}