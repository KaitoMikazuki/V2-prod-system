console.log("i am alive")

window.addEventListener('DOMContentLoaded', displayCompleted)

const tdl_button = document.getElementById("tdl-button");

tdl_button.addEventListener('click', async function(){
    await fetch('/tdl', {method: "POST"}) ; // Calls the route only
    displayCompleted();
})

async function displayCompleted(){
    const res = await fetch('pass_totaltdl');
    let data = await res.json();
    data = Math.floor(data["total_tdl"]/100)
    console.log(data)
    tdl_completed = document.getElementById("tdl-completed");
    tdl_completed.textContent = `${data}`;
}