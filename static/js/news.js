const apiKey = '4cb2e24fe1374c6c8a8483f36b69186f';
const newsContainer = document.querySelector('.news-container');
const maxNews = 5; // Number of news articles to display

function fetchNews() {
  // const url = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=4cb2e24fe1374c6c8a8483f36b69186f'; // Example fetching top India news
  const url = 'https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=4cb2e24fe1374c6c8a8483f36b69186f'; // Example fetching top India news

  fetch(url)
    .then(response => response.json())
    .then(data => {
      const articles = data.articles.slice(0, maxNews); // Get only the first 5 articles
      displayNews(articles);
    })
    .catch(error => {
      console.error('Error fetching news:', error);
    });
}

function displayNews(articles) {
  newsContainer.innerHTML = '';
  articles.forEach(article => {
    const newsItem = document.createElement('div');
    newsItem.classList.add('news-item');

    // Wrap news item in a link (same logic as previous example)
    const newsLink = document.createElement('a');
    newsLink.href = article.url;
    newsLink.target = '_blank'; // Open in a new tab
    newsItem.appendChild(newsLink);

    if (article.urlToImage) {
      const image = document.createElement('img');
      image.src = article.urlToImage;
      image.alt = article.title;
      image.classList.add('news-image');
      newsLink.appendChild(image); // Add image inside the link
    }

    const title = document.createElement('h3');
    title.textContent = article.title;
    title.classList.add('news-title');
    newsLink.appendChild(title); // Add title inside the link

    newsContainer.appendChild(newsItem);
  });
}

fetchNews();
