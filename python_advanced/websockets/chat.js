// Connexion au serveur WebSocket
const socket = new WebSocket("ws://localhost:8000/ws");

const messagesDiv = document.querySelector("#messages");
const input = document.querySelector("#message-input");
const sendButton = document.querySelector("#send-button");
const status = document.querySelector("#status");

// Affiche un message dans la zone de chat
function displayMessage(text, type) {
  const div = document.createElement("div");
  div.className = "message " + type;
  div.textContent = text;
  messagesDiv.appendChild(div);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Envoie le contenu de l'input au serveur
function sendMessage() {
  const text = input.value.trim();
  if (text === "") {
    return;
  }
  socket.send(text);
  displayMessage(text, "sent");
  input.value = "";
}

// Connexion établie
socket.onopen = () => {
  status.textContent = "Connecté";
  status.className = "connected";
};

// Message reçu du serveur
socket.onmessage = (event) => {
  displayMessage(event.data, "received");
};

// Connexion perdue
socket.onclose = () => {
  status.textContent = "Connexion perdue";
  status.className = "disconnected";
};

// Clic sur le bouton Envoyer
sendButton.addEventListener("click", sendMessage);

// Touche Entrée dans l'input
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    sendMessage();
  }
});
