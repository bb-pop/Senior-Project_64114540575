function searchItems() {
    let input = document.getElementById('searchInput');
    let filter = input.value.toUpperCase();
    let itemContainer = document.getElementsByClassName('container')[0];
    let items = itemContainer.getElementsByClassName('item-background');
    for (let i = 0; i < items.length; i++) {
        let itemName = items[i].getElementsByClassName('item-name')[0];
        if (itemName) {
            let textValue = itemName.textContent || itemName.innerText;
            if (textValue.toUpperCase().indexOf(filter) > -1) {
                items[i].style.display = "";
            } else {
                items[i].style.display = "none";
            }
        }       
    }
}