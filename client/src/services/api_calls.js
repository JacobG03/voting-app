export async function getData(endpoint) {
  const response = await fetch(endpoint, {
    method: 'GET',
    mode: 'cors',
    credentials: 'same-origin',
  })
  .then(r => r.json().then(data => ({status: r.status, body:data})))
  return response;
}


export async function postData(endpoint, data={}) {
  const response = await fetch(endpoint, {
    method: 'POST',
    mode: 'cors',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  return response.json();
}