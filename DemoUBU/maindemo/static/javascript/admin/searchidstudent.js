function searchItems() {
    let input = document.getElementById('searchInput');
    let filter = input.value.toUpperCase();
    let tableContainer = document.getElementsByClassName('table-container')[0];
    let rows = tableContainer.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        let idCell = rows[i].getElementsByClassName('id-student')[0];
        if (idCell) {
            let textValue = idCell.textContent || idCell.innerText;
            if (textValue.toUpperCase().indexOf(filter) > -1) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    }
}

function enterSearch(event) {
    if (event.keyCode === 13) {
        searchItems();
    }
}