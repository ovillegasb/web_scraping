let = $accordion = document.getElementById("accordion");

//let articles_Data = null;

//fetch('./articles.json')
//  .then(function (response) {
//    return response.json();
//  })
//  .then(function (data) {
//    appendData(data);
//  })
//  .catch(function (err) {
//    console.log(err)
//  })
//"https://app.scrapinghub.com/api/v2/datasets/kdybI1E79Ww/download?format=json"
fetch('./articles.json')
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    // Work with JSON data here
    articles_Data = data;
    cards = articles_Data.map(
      (x, idx) => `
    <div class="card">
    <div class="card-header bg-dark" id="heading${idx}">
      <h2 class="mb-0">
        <button
          class="btn btn-outline-light"
          type="button"
          data-toggle="collapse"
          data-target="#collapse${idx}"
          aria-expanded="true"
          aria-controls="collapse${idx}"
        >
          ${x.title}
        </button>
      </h2>
    </div>

    <div
      id="collapse${idx}"
      class="collapse"
      aria-labelledby="heading${idx}"
      data-parent="#accordion"
    >
      <div class="card-body">
        ${x.abstract}
        <br>
        <br>
        <a href=${x.url} target="_blank">Ver más</a>
      </div>
    </div>
  </div>
    `
    );
    for (i = 0; i < cards.length; i++) {
      $accordion.innerHTML += cards[i];
    }
  })
  .catch((err) => {
    // console.log('Do something for an error here')
  });
