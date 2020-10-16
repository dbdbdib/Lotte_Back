var scrap_list = document.querySelectorAll('.scrap')
console.log(scrap_list)
Array.from(scrap_list).forEach(item => {
    item.addEventListener('click', scrap, false);
});
function scrap(e) {
    console.log(e.target.nextSibling.nextSibling.nextSibling.nextSibling)
    fetch('/scrap/' + e.target.nextSibling.nextSibling.value, {
        method: 'get',
        headers: {
            'Accept': 'application/json'
        }
    }).then((res) => {
        if (res.status === 200 || res.status === 201) {
            res.json().then((json) => {
                console.log("성공", json)
                if (json['flag'] === "None") {
                    e.target.innerHTML = "🖤"
                } else {
                    e.target.innerHTML = "🧡"
                }
                e.target.nextSibling.nextSibling.nextSibling.nextSibling.innerHTML = "(" + json["len"] + ")"
            },
            )
        } else {
        }
    }).catch(err => console.error(err));
}

