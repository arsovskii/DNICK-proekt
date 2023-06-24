// toSend=["dada"];
// $.ajax("/posttag/",{
//                 type:"POST",
//                 data:JSON.stringify(toSend),
//                 dataType: 'application/json'
//             })
// document.addEventListener("DOMContentLoaded", () => {
//     let tagForm = document.getElementById("formTag").children[1]
//     let tagSubmit = document.getElementById("submitTag");
//     let gameId = document.getElementById("gameid").innerText;
//
//     let cookie = document.cookie
//     let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
//
//
//     tagSubmit.addEventListener("click", () => {
//         if (tagForm.value !== "") {
//             let toSend = [{"game": gameId}, {"tag":tagForm.value}]
//
//             $.ajax("/posttag/",{
//                 type:"POST",
//                 data:JSON.stringify(toSend),
//                 dataType: 'application/json'
//             })
//             // fetch("/posttag/", {
//             //     method: "post",
//             //     cache: "no-cache",
//             //     headers: {
//             //         'Content-Type':"application/json",
//             //         'X-CSRFToken': csrfToken
//             //     },
//             //     body: JSON.stringify(toSend),
//             // }).then((res) => {
//             //     console.log(res)
//             // })
//         }
//
//     })
// })
//
//
//

$(document).ready(() => {

    let tagForm = document.getElementById("formTag").children[1]
    let tagSubmit = document.getElementById("submitTag");
    let gameId = document.getElementById("gameid").innerText;

    let cookie = document.cookie
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    let tagList = document.getElementById("tagList");


    tagSubmit.addEventListener("click", () => {
        if (tagForm.value !== "") {
            let toSend = [{"game": gameId}, {"tag": tagForm.value}]

            $.ajax("/posttag/", {
                type: "POST",
                data: JSON.stringify(toSend),
                headers: {
                    'Content-Type': "application/json",
                    'X-CSRFToken': csrfToken
                },
                dataType: "json",
                success: (resp) => {
                    // console.log(resp)
                    rows = resp['tags']
                    addRows(rows);
                }
            })

        }

    })
})

function addRows(rows) {

    tagList.innerHTML = "";

    for (let i = 0; i < rows.length; i++) {

        const li = document.createElement("li");
        const text = document.createTextNode(rows[i]);
        li.className = "list-group-item";
        li.appendChild(text);

        tagList.append(li);

    }
}
