const BASE_URL = "http://localhost:3000/web/users";

async function loadUsers() {
  const response = await fetch(BASE_URL);
  const users = await response.json();

  const list = document.getElementById("usersList");
  list.innerHTML = "";

  users.forEach(user => {
    const item = document.createElement("li");

    item.innerText = `${user.id}: ${user.name} (${user.email})`;

    list.appendChild(item);
  });
}

async function addUser() {
  const user = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value
  };

  await fetch(BASE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(user)
  });

  await loadUsers();
}
