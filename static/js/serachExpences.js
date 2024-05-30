const searchField = document.querySelector("#searchField");
const appTable = document.querySelector(".app-table"); // complete table
const paginationContainer = document.querySelector(".pagination-container"); // for pagination
const tableOutput = document.querySelector(".table-output"); //for column name of result
const tbody = document.querySelector(".table-body"); // content inside column
const noResult_text = document.querySelector(".no-results");

tableOutput.style.display = "none";

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;
  noResult_text.style.display = "none";
  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    appTable.style.display = "none";
    tbody.innerHTML = "";
    fetch("/expenses/search-expenses/", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        
        tableOutput.style.display = "block";

        console.log("data.length", data.length);
        if (data.length === 0) {
          noResult_text.style.display = "block";
        } else {
          data.forEach((item) => {
            tbody.innerHTML += `
                <tr>
                <td>${item.amount}</td>
                <td>${item.category}</td>
                <td>${item.description}</td>
                <td>${item.date}</td>
                </tr>`;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});
