const ws = new WebSocket("ws://localhost:8000/ws");

let currentUser = "";
let typingTimeout;
let typingElementId = "typing-msg";


// RECEIVE MESSAGE
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const chat = document.getElementById("chat");
    const typingDiv = document.getElementById("typingIndicator");

    if (data.type === "system") {
            chat.innerHTML += `
        <div class="message system">
            <div class="bubble system-bubble">
            ${data.message}
            </div>
        </div>
        `;
    }

    else if (data.type === "chat") {
    const isMe = data.username === currentUser;

    chat.innerHTML += `
    <div class="message ${isMe ? 'me' : 'other'}">
        <div class="bubble">
        <b>${data.username}:</b> ${data.message}
        </div>
    </div>
    `;
    }

    else if (data.type === "typing") {
        const chat = document.getElementById("chat");

        // remove old typing if exists
        const existing = document.getElementById(typingElementId);
        if (existing) existing.remove();

        // add new typing message
        const typingHTML = `
            <p id="${typingElementId}" class="message typing-msg">
            ${data.username} is typing...
            </p>
        `;

        chat.innerHTML += typingHTML;

        chat.scrollTop = chat.scrollHeight;

        // remove after delay
        clearTimeout(typingTimeout);
        typingTimeout = setTimeout(() => {
            const el = document.getElementById(typingElementId);
            if (el) el.remove();
        }, 1000);
    }

    //  USER LIST
    else if (data.type === "users") {
        const usersText = data.users.join(", ");
        document.getElementById("users").innerText = `Online: ${usersText}`;
    }

    else if (data.type === "private") {
        const chat = document.getElementById("chat");

        const isMe = data.self === true;

        if (isMe) {
            //  My private message (right side)
            chat.innerHTML += `
            <p class="message private me">
                <b>(To ${document.getElementById("toUser").value}) You:</b> ${data.message}
            </p>
            `;
        } else {
            //  Received private message (left side)
            chat.innerHTML += `
            <p class="message private other">
                <b>(Private) ${data.from}:</b> ${data.message}
            </p>
            `;
        }

        chat.scrollTop = chat.scrollHeight;
    }

    else if (data.type === "search_results") {
        const resultsDiv = document.getElementById("searchResults");

        resultsDiv.innerHTML = ""; // clear old results

        if (data.results.length === 0) {
            resultsDiv.innerHTML = "<p>No results found</p>";
            return;
        }

        data.results.forEach(msg => {
            resultsDiv.innerHTML += `
            <div class="search-item">
                <b>${msg.username}:</b> ${msg.message}
            </div>
            `;
        });
    }

    chat.scrollTop = chat.scrollHeight;
    };

    // JOIN
    function join() {
    const username = document.getElementById("username").value;
    const room = document.getElementById("room").value;

    if (!username || !room) {
        alert("Enter username and room");
        return;
    }

    currentUser = username;
    document.getElementById("roomName").innerText = `Room: ${room}`;

    ws.send(JSON.stringify({
        type: "join",
        username: username,
        room: room
    }));

     //  hide join
  document.getElementById("joinSection").style.display = "none";

  //  show chat + search
  document.getElementById("mainContainer").style.display = "flex";
}

// SEND
function send() {
  const msgInput = document.getElementById("msg");
  const msg = msgInput.value;
  const toUser = document.getElementById("toUser").value;

  if (!msg) return;

  //  PRIVATE MESSAGE
  if (toUser) {
    ws.send(JSON.stringify({
      type: "private",
      to: toUser,
      message: msg
    }));

    document.getElementById("toUser").value = "";

  } 
  else {
    // normal chat
    ws.send(JSON.stringify({
      type: "chat",
      username: currentUser,
      message: msg
    }));
  }

  msgInput.value = "";
}


function searchMessages() {
  const keyword = document.getElementById("searchInput").value.trim();

  if (!keyword) {
    alert("Enter something to search");
    return;
  }

  ws.send(JSON.stringify({
    type: "search",
    keyword: keyword
  }));
}

function clearSearch() {
  document.getElementById("searchResults").innerHTML = "";
  document.getElementById("searchInput").value = "";
}


document.getElementById("msg").addEventListener("input", () => {
  ws.send(JSON.stringify({
    type: "typing"
  }));
});

// ENTER KEY SUPPORT
document.addEventListener("DOMContentLoaded", () => {
  const msgInput = document.getElementById("msg");

  msgInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
      send();
    }
  });
});

document.getElementById("searchInput").addEventListener("keypress", function(e) {
  if (e.key === "Enter") {
    searchMessages();
  }
});
