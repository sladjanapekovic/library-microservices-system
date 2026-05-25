const BASE_URL = "http://localhost:3000/web/borrowings";

async function loadBorrowings() {
  const response = await fetch(BASE_URL);
  const borrowings = await response.json();

  const list = document.getElementById("borrowingsList");
  list.innerHTML = "";

  borrowings.forEach(borrowing => {
    const item = document.createElement("li");

    item.innerHTML = `
      ID: ${borrowing.id},
      User ID: ${borrowing.userId},
      Book ID: ${borrowing.bookId},
      Returned: ${borrowing.returned}
    `;

    list.appendChild(item);
  });
}

async function createBorrowing() {
  const borrowing = {
    userId: Number(document.getElementById("userId").value),
    bookId: Number(document.getElementById("bookId").value)
  };

  await fetch(BASE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(borrowing)
  });

  await loadBorrowings();
}
