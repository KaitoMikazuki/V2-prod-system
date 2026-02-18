updateGraph(); //On load
dialog = document.getElementById("dialog")

const dialogButton = document.getElementById("add-filters");
dialogButton.addEventListener("click", openDialog)

const closeButton = document.getElementById("closeButton")
closeButton.addEventListener("click", closeDialog)

dialogForm = document.getElementById("dialogForm")
dialogForm.addEventListener("submit", handleForm)

async function updateGraph(data){
    const response = await fetch("/update_statistics");
    if (!response.ok) throw new Error(response.status);
    const fig = await response.json();
    console.log(fig)
    // The id of the chart is "#graph"
    Plotly.react("graph", fig.data, fig.layout)
}

function openDialog(){
    dialog.showModal()
}

function closeDialog(){
    dialog.close();
}

// async function handleForm(event){
//     const response = await fetch("/update_statistics");
//     if (!response.ok) throw new Error(response.status);
//     const data = await response.json;
// }

// Suggested that i replace the graph's data instead of refreshing