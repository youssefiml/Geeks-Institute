import axios from 'axios';

function fetchPosts() {
    return axios.get('https://jsonplaceholder.typicode.com/posts');
};


export { fetchPosts };