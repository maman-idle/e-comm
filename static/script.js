function showPendingOrders() {
  const orders = document.querySelector(".pending_opt");

  if (orders.classList.contains("hide")) {
    orders.classList.remove("hide");
  } else {
    orders.classList.add("hide");
  }
  return false;
}

function showDeliveredOrders() {
  const orders = document.querySelector(".delivered_opt");

  if (orders.classList.contains("hide")) {
    orders.classList.remove("hide");
  } else {
    orders.classList.add("hide");
  }
}

function buy() {
  const buy = document.querySelector(".buy_opt");

  if (buy.classList.contains("hide")) {
    buy.classList.remove("hide");
  } else {
    buy.classList.add("hide");
  }
}

function showProducts() {
  const buy = document.querySelector(".products_opt");

  if (buy.classList.contains("hide")) {
    buy.classList.remove("hide");
  } else {
    buy.classList.add("hide");
  }
}

function showCustomers() {
  const buy = document.querySelector(".customers_opt");

  if (buy.classList.contains("hide")) {
    buy.classList.remove("hide");
  } else {
    buy.classList.add("hide");
  }
}

function search_bar1() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("keyword1");
  filter = input.value.toUpperCase();
  table = document.getElementById("my_table1");
  tr = document.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function search_bar2() {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("keyword2");
  filter = input.value.toUpperCase();
  table = document.getElementById("my_table2");
  tr = document.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
