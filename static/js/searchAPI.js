function searchShow(query) {
    const base_url = `https://api.tvmaze.com/search/shows?q=${query}`;
    //this is requesting a list of objects from the api
    fetch(base_url)
    .then(function(res) {
        return res.json();
    })
    //this prints the data in the DOM
    .then(function(jsonData){
        const results = jsonData.map(element => element.show.name);
        console.log(results);
    })
};