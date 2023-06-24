var name;
var img;
var id;
var developer;
var price;

const searchForm = document.getElementById("searchForm")
const typeSort = document.getElementById("typeSort");
const genre = document.getElementById("genre-select");


typeSort.addEventListener("change",()=>{
    searchForm.submit();
})

genre.addEventListener("change",()=>{
    searchForm.submit();
})



searchForm.addEventListener("keypress", (e) => {

    if (e.key.toLowerCase() === "enter") {
        searchForm.submit();
    }
})

new Autocomplete('#autocomplete', {
    search: input => {
        const url = `/search/?query=${input}`;

        return new Promise(resolve => {
            fetch(url).then(response => {
                response.json().then(data => {

                    resolve(data.query);
                })
            })
        })
    },
    debounceTime: 700,

    onSubmit: result => {
        name = result.name;
        img = result.img;
        id = result.id;
        price = result.price;
        developer = result.developer;
        document.location.href = `/games/${developer}/${id}`;
    },
    autoSelect: false,

    renderResult: (result, props) => `
    <li ${props} >
    <div class="d-flex flex-row">
        <div style="width: 150px;">
            <img src="${result.img}" style="width:150px; height:100%; aspect-ratio:21/9; object-fit: cover ">
        </div>
      <div class="d-flex flex-column ms-4 fs-4">
      <span class=" ">
        ${result.name}
      </span>
      <span class="fs-5 text-muted fst-italic">${result.price} ден.</span>
      </div>
      </div>
    </li>`,

    getResultValue: result => result.name
})




