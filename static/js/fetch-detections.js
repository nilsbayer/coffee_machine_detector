const search_result_container = document.getElementById("container")
const results_holder = document.getElementById("results-holder")

window.addEventListener("load", () => {
    // actual code
    // check whether model detected a machine
    setInterval(() => {

        fetch("/detection", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            }
            // body: JSON.stringify({
            //     something: something
            // })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Data", data)
            if (data.data_length > 0) {
                // forEach detected machine append html tags
                let detected_machines = data.items
                results_holder.innerHTML = ""
                detected_machines.forEach(machine => {
                    let search_result = document.createElement("div")
                    search_result.classList.add("search-result")
                    search_result.innerHTML = `
                        <img width="25%" src=${machine.img_path} alt="">
                        <div>
                            <span class="result-title">${machine.name}</span>
                            <p class="result-text">${machine.info_text}</p>
                        </div>
                    `
                    let search_result_outer = document.createElement("a")
                    search_result_outer.setAttribute("href", `http://localhost:5000/explore/${machine.link}`)
                    search_result_outer.append(search_result)
                    results_holder.append(search_result_outer)
                    console.log(search_result_outer)
                }); 

                setTimeout((e) => {
                    search_result_container.style.bottom = "0"
                }, 100)
                search_result_container.style.maxHeight = "50vh"
            }
            else {
                setTimeout((e) => {
                    search_result_container.style.bottom = "-20rem"
                }, 100)
                search_result_container.style.maxHeight = "0"
            }
            
        })

    }, 500);

})