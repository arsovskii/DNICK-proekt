let form = document.getElementById("pictureForm");
let paragraph = document.getElementById("pictureP");

if (paragraph !== null) {

    form.getElementsByTagName("input")[1].addEventListener('change', () => {
        paragraph.innerText = ("Сликата е поставена");
        form.submit();
    })

}
