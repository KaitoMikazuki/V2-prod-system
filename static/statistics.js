dialog = document.getElementById("dialog")

const dialogButton = document.getElementById("add-filters");
dialogButton.addEventListener("click", openDialog)

const closeButton = document.getElementById("closeButton")
closeButton.addEventListener("click", closeDialog)

function openDialog(){
    dialog.showModal()
}

function closeDialog(){
    dialog.close();
}

