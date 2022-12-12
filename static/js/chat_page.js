window.addEventListener('load', setup);

var messages = "";
var chat_window;

function setup() {
    chat_window = document.getElementById("window");
    getMessages()
}

function newMessage() {
    let message = document.getElementById('message').value;
    let author = document.getElementById('username').innerText;

    author = author.substring(author.indexOf(':') + 2);
    fetch("/new_message/", {
        method: "POST",
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
        body: `message=${message}&author=${author}`
    })
        .then((response) => response.json())
        .then((results) => {
            let current_set = results[0];
            let temp = `<p> ${current_set['author']}: ${current_set['message']}</p>`;
            chat_window.innerHTML += temp;
        })
        .catch((e) => {
            console.log('Error sending new messaage to db: ', e)
        })
}


function getMessages() {
    fetch("/messages/")
        .then((response) => response.json())
        .then((results) => {
            var messages = "";
            for (index in results) {
                let m = results[index];
                messages += `<p> ${m['author']}: ${m['message']}</p>`;
            }
            chat_window.innerHTML = messages;
        })
        .catch(() => {
            chat_window.innerHTML = "<p class='err'>Failed to retrieve messages from server<p>";
        })
    setInterval(getMessages, 2000);
};