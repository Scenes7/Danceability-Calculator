let form = document.getElementById('uploadForm');
let browseBtn = document.getElementById('browseButton');
let finput = document.getElementById('selectFile');
let bpmTitle = document.getElementById('bpmTitle');
let bpmResult = document.getElementById('bpmResult');
let tempoTitle = document.getElementById('tempoTitle');
let tempoResult = document.getElementById('tempoResult');
let ratingTitle = document.getElementById('ratingTitle');
let ratingResult = document.getElementById('ratingResult');
let errorp = document.getElementById('error');
let closeButton = document.getElementById('closeButton');
let infoDiv = document.getElementById('infoDiv');
let openButton = document.getElementById('openButton');

const titlesObj = [bpmTitle, tempoTitle, ratingTitle]
const resultsObj = [bpmResult, tempoResult, ratingResult]

infoDiv.style.display = 'none';

browseBtn.addEventListener('click', () => {
  finput.click();
})

openButton.addEventListener('click', () => {
  if (infoDiv.style.display == 'none') infoDiv.style.display = 'block';
  else infoDiv.style.display = 'none';
})

closeButton.addEventListener('click', () => {
  if (infoDiv.style.display == 'none') infoDiv.style.display = 'block';
  else infoDiv.style.display = 'none';
})

form.addEventListener('submit', handleFormSubmit);


form.addEventListener('change', () => {
  browseBtn.innerHTML = finput.files[0].name
  console.log(finput.files)
})

function postWavFile(url, file, callback) {
  var xhr = new XMLHttpRequest();
  var formData = new FormData();

  formData.append("file", file);

  xhr.open("POST", url, true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        callback(xhr.responseText, 200);
      } else {
        callback(new Error("Request failed with status "), xhr.status);
      }
    }
  };
  xhr.onerror = function () {
    callback(new Error("Request failed"));
  };
  xhr.send(formData);
}

function handleFormSubmit(event) {
  event.preventDefault();
  errorp.style.color = 'black';
  errorp.style.display = 'block';
  errorp.innerHTML = "Processing...";
  console.log("A")
  let url = "http://127.0.0.1:5000/upload";
  let fileInput = document.getElementById("selectFile");
  if (fileInput.files[0] == null) {
    errorp.style.color = 'darkred';
    afterSubmit('*select a mp3 or wav file')
    return
  }
  console.log("A")
  var file = fileInput.files[0]
  console.log("F")
  postWavFile(url, file, function (error, response) {
    errorp.style.color = 'darkred';
    errorp.style.display = 'none';
    errorp.innerHTML = "";
    if (response != 200) {
      console.log(error, response, " FFG", Object.keys(error))
      if (response == 415) afterSubmit('file must be of type mp3 or wav')
      else if (response == 413) afterSubmit('Song must be under 10 minutes')
      else afterSubmit('something went wrong, try again later')
    } else {
      errorp.style.display = 'none';
      displayResults(error);
    }
  });
  console.log("G")
}

const sleep = ms => new Promise(async r => setTimeout(r, ms));

function afterSubmit(s) {
  errorp.style.display = 'block';
  errorp.innerHTML = s;
}

async function numberAnimation(obj, target, idx) {
  for (let i = 0; i<=target; i++) {
    if (idx > 0) obj.innerHTML = i+"%";
    else obj.innerHTML = i;
    await sleep(Math.round(1000/target));
  }
}
async function displayResults(responseString) {
  let results = responseString.split('|');
  // results[2] = 85; results[1] = 55
  for (let i = 0; i<3; i++) {
    titlesObj[i].style.display = "block";
    titlesObj[i].classList.add('fade');
    await sleep(500);
    resultsObj[i].style.display = "block";
    resultsObj[i].classList.add('fade');
    numberAnimation(resultsObj[i], results[i], i);
  }

}