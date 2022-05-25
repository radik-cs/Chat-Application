document.addEventListener('DOMContentLoaded', () => {


    console.log("Loaded")

    msg_form = document.getElementById('new_msg_form')
    msg_form.addEventListener('submit', function (event) {
        event.preventDefault();

        username = document.getElementById('username').innerHTML;
        message = document.getElementById('message').value;
        console.log(`${username}, ${message}`);

        fetch('/new_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded', charset: 'utf8' },
            body: `username=${username}&message=${message}`
        }).then(response => response.json())
            .then(data => {
                console.log(data)
                document.getElementById('message').value = ''
            })
            .catch((error) => {
                console.log(error)
            });


    })
    let chat_window = document.getElementById('messages');
    function fetch_messages() {
        fetch('/messages').then(response => response.json())
            .then(results => {
                console.log(results)

                let messages = ""

                for (let index in results) {
                    //console.log(index)
                    let current_set = results[index]
                    console.log(current_set)
                    for (let i in current_set) {
                        // console.log(current_set[i])
                        author = current_set[i]["author"]
                        id = current_set[i]["id"]
                        message = current_set[i]["message"]

                        messages += `${author}:\n${message}\n\n`;

                    }


                }

                chat_window.value = messages;
            })
            .catch((error) => {
                chat_window.value = "error retrieving messages from server";
            });

    }

    setInterval(fetch_messages, 15000)


});