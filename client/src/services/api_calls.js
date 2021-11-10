const api = 'https://voting-app2.herokuapp.com/api'

export async function getData(endpoint) {
  const response = await fetch(api + endpoint, {
    method: 'GET',
    mode: 'cors',
    credentials: 'same-origin',
  })
  .then(r => r.json().then(data => ({status: r.status, body:data})))
  return response;
}


export async function postData(endpoint, data={}) {
  const response = await fetch(api + endpoint, {
    method: 'POST',
    mode: 'cors',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(r => r.json().then(data => ({status: r.status, body:data})))
  return response;
}