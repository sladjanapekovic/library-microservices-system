const BASE_URL = "http://localhost:3000/web/books";

// Load all books
async function loadBooks() {
  const res = await fetch(BASE_URL);
  const data = await res.json();

  const list = document.getElementById("booksList");
  list.innerHTML = "";

  data.forEach(book => {
    const li = document.createElement("li");
    li.innerText = `${book.title} - ${book.author}`;
    list.appendChild(li);
  });
}

// Add book
async function addBook() {
  const title = document.getElementById("title").value;
  const author = document.getElementById("author").value;
  const genre = document.getElementById("genre").value;
  const copies = document.getElementById("copies").value;

  await fetch(BASE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      title,
      author,
      genre,
      available_copies: Number(copies)
    })
  });

  loadBooks();
}
