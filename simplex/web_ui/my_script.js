function handleSolve(){
    let type = document.getElementById('type').value 
    let objective = document.getElementById('objective').value 
    let constraints = document.getElementById('constraints').value 
    let naturalSolution = false
    if (document.getElementById('naturalSolution').checked){
      naturalSolution = true
    }
    let url = 'http://localhost:5000/simplex-solver/api/solve'
    let data = {
      objective: type+" "+objective,
      constraints: constraints,
      naturalSolution: naturalSolution
    }

    // Send a POST request to the Flask backend
    fetch(url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        // Update the result element with the response from the server
        console.log(data)
        document.getElementById('result').innerText = JSON.stringify(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });

    // code to send rest api request 
}