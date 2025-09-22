let quotes = [
    { id: 0, author: "Albert Einstein", quote: "Life is like riding a bicycle. To keep your balance, you must keep moving.", likes: 0 },
    { id: 1, author: "Maya Angelou", quote: "You will face many defeats in life, but never let yourself be defeated.", likes: 0 },
    { id: 2, author: "Steve Jobs", quote: "Innovation distinguishes between a leader and a follower.", likes: 0 },
    { id: 3, author: "Albert Einstein", quote: "Imagination is more important than knowledge.", likes: 0 },
    { id: 4, author: "Maya Angelou", quote: "If you don't like something, change it. If you can't change it, change your attitude.", likes: 0 }
];
let currentQuote = null;
let lastQuoteId = null;
let filteredQuotes = [];
let currentFilterIndex = 0;
function generateQuote() {
    let randomQuote;
    do {
        randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
    } while (randomQuote.id === lastQuoteId && quotes.length > 1);
    
    currentQuote = randomQuote;
    lastQuoteId = randomQuote.id;
    
    document.getElementById('quote-section').innerHTML = `
        <div class="quote-text">"${randomQuote.quote}"</div>
        <div class="quote-author">- ${randomQuote.author} (Likes: ${randomQuote.likes})</div>
    `;
    
    document.getElementById('quote-buttons').style.display = 'block';
    document.getElementById('stats').style.display = 'none';
}
function addQuote(event) {
    event.preventDefault();
    
    const newQuoteText = document.getElementById('new-quote').value;
    const newAuthor = document.getElementById('new-author').value;
    
    const newId = quotes.length;
    quotes.push({
        id: newId,
        author: newAuthor,
        quote: newQuoteText,
        likes: 0
    });
    
    document.getElementById('new-quote').value = '';
    document.getElementById('new-author').value = '';
    
    alert('Quote added successfully!');
}
function countCharsWithSpaces() {
    if (currentQuote) {
        const count = currentQuote.quote.length;
        showStats(`Characters (with spaces): ${count}`);
    }
}
function countCharsWithoutSpaces() {
    if (currentQuote) {
        const count = currentQuote.quote.replace(/\s/g, '').length;
        showStats(`Characters (without spaces): ${count}`);
    }
}
function countWords() {
    if (currentQuote) {
        const count = currentQuote.quote.trim().split(/\s+/).length;
        showStats(`Word count: ${count}`);
    }
}
function likeQuote() {
    if (currentQuote) {
        currentQuote.likes++;
        generateQuote();
        showStats(`Quote liked! Total likes: ${currentQuote.likes}`);
    }
}
function showStats(message) {
    document.getElementById('stats').innerHTML = message;
    document.getElementById('stats').style.display = 'block';
}
function filterByAuthor(event) {
    event.preventDefault();
    
    const authorName = document.getElementById('filter-author').value.toLowerCase();
    filteredQuotes = quotes.filter(quote => 
        quote.author.toLowerCase().includes(authorName)
    );
    
    if (filteredQuotes.length === 0) {
        alert('No quotes found for this author!');
        return;
    }
    
    currentFilterIndex = 0;
    showFilteredQuote();
    document.getElementById('filter-results').style.display = 'block';
}
function showFilteredQuote() {
    const quote = filteredQuotes[currentFilterIndex];
    document.getElementById('filtered-quote').innerHTML = `
        <div class="quote-text">"${quote.quote}"</div>
        <div class="quote-author">- ${quote.author} (Likes: ${quote.likes})</div>
    `;
    
    document.getElementById('filter-counter').innerHTML = 
        `Quote ${currentFilterIndex + 1} of ${filteredQuotes.length}`;
}
function previousFilteredQuote() {
    if (filteredQuotes.length > 0) {
        currentFilterIndex = (currentFilterIndex - 1 + filteredQuotes.length) % filteredQuotes.length;
        showFilteredQuote();
    }
}
function nextFilteredQuote() {
    if (filteredQuotes.length > 0) {
        currentFilterIndex = (currentFilterIndex + 1) % filteredQuotes.length;
        showFilteredQuote();
    }
}