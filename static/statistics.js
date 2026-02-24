updateGraph(on_load = true); //On load

const dialogForm = document.getElementById("dialogForm")
dialogForm.addEventListener("submit", () => {
    updateGraph();
})


dialog = document.getElementById("dialog")

const dialogButton = document.getElementById("add-filters");
dialogButton.addEventListener("click", openDialog)

const closeButton = document.getElementById("closeButton")
closeButton.addEventListener("click", closeDialog)

async function updateGraph(on_load = false){
    let filters;
    console.log(on_load)
    if (on_load === true){
        filters = {on_load: true}
    }
    
    else if (on_load === false){
        filters = await handleForm(dialogForm)
        filters.on_load = false
    }

    const response = await fetch("/update_statistics", {
        method: "POST",
        headers:{
            "Content-type": "application/json"
        },
        body: JSON.stringify(filters)
    })
    if (!response.ok) throw new Error(response.status);
    const fig = await response.json();
    // The id of the chart is "#graph"
    Plotly.react("graph", fig.data, fig.layout)
}

function openDialog(){
    dialog.showModal()
}

function closeDialog(){
    dialog.close();
}

async function handleForm(form){
    const formData = new FormData(form);
    let filters = {
        work_type: formData.getAll('workType'),
        label: null, // REVISIT: Feature not yet rolled out so null
        period_start: formData.get('periodStart'),
        period_end: formData.get('periodEnd'),
    }
    console.log(filters)
    return filters
}