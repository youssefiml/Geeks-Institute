const allBooks = [
    {title: "Harry Potter", author: "J.K. Rowling", image: "https://via.placeholder.com/100", alreadyRead: true},
    {title: "The Hobbit", author: "J.R.R. Tolkien", image: "https://via.placeholder.com/100", alreadyRead: false}
];

const section = document.querySelector(".listBooks");

allBooks.forEach(book => {
    const div = document.createElement("div");
    div.innerHTML = `<p>${book.title} written by ${book.author}</p>`;
    const img = document.createElement("img");
    img.src = book.image;
    div.appendChild(img);
    if (book.alreadyRead) div.style.color = "red";
    section.appendChild(div);
});