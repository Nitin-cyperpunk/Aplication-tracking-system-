// script.js
const form = document.getElementById('resumeForm');
const resultsContainer = document.getElementById('results');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const jobDescription = document.getElementById('jobDescription').value;
  const resumeFile = document.getElementById('resumeFile').files[0];

  if (!jobDescription || !resumeFile) {
    alert('Please enter job description and upload a resume file.');
    return;
  }

  const formData = new FormData();
  formData.append('jobDescription', jobDescription);
  formData.append('resumeFile', resumeFile);

  try {
    const response = await fetch('/evaluate', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      const result = await response.json();
      displayResults(result);
    } else {
      displayError('An error occurred while evaluating the resume.');
    }
  } catch (error) {
    displayError('An error occurred while evaluating the resume.');
  }
});

function displayResults(result) {
  resultsContainer.innerHTML = `
    <h3>Resume Review</h3>
    <p>${result.review}</p>
    <h3>Job Suggestions</h3>
    <p>${result.jobSuggestions}</p>
  `;
}

function displayError(message) {
  resultsContainer.innerHTML = `<p class="text-danger">${message}</p>`;
}