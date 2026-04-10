const API = "http://127.0.0.1:8000";

async function validateResponse(response, message) {
  const data = await response.json();

  if (!response.ok) {
    // backend sent error message
    throw new Error(data.detail || message);
  }

  return data;
};

// JSON.stringify(): JS → JSON (to backend)
// res.json(): JSON → JS (from backend)

// export const getbalance -> this represents a function decloration
// We are exporting(like godot) a constant function that returns fetch

// (userID) => -> this is an arrow function which is the same things as:
//          function getBalance(userID) {return fetch()}
// userID is the paramater/input

// fetch is a built in function that makes an HTTP request("pings" api.py/ "pings" the endpoints)
// by default, it is a GET requets so: fetch(`${API}/balance/${userId}`) -> returns the value of GET /balance/{user_id} endpoint
//      however, it doesn't return the actual data

// res = the HTTP response(the value of fetch/the promise).
// by arrow function logic: res => res.json = function ___() {return res.json()}
//      res.json() converts the HTTP response into a JavaScript object
export const getBalance = (userId) => {
  fetch(`${API}/balance/${userId}`).then(res => res.json());
  return validateResponse(res, "Balance retrieval failed");
}

export const createUser = async(userName, email) => {
    const res = await fetch(`${API}/create-user`, 
    { // because POST/deposit/ takes a "deposite" object, we have to convert the data
        method: "POST", // clarifies a post request
        headers: { "Content-Type": "application/json" }, // Tells the api that the data is JSON
        body: JSON.stringify(
          { 
            "name": userName, 
            "email": email
          }
        ) // converst JS object to JSON string(opposite of res.json())
    });

    return validateResponse(res, "User creation failed");
}

export const deposit = async (userID, amount) => {
    const res = await fetch(`${API}/deposit`, 
    { // because POST/deposit/ takes a "deposite" object, we have to convert the data
        method: "POST", // clarifies a post request
        headers: { "Content-Type": "application/json" }, // Tells the api that the data is JSON
        body: JSON.stringify(
          { 
            "user_id": userID, 
            "amount": amount
          }
        ) // converst JS object to JSON string(opposite of res.json())
    });

  return validateResponse(res, "Deposit failed");
}

export const withdraw = async (userID, amount) => {
    const res = await fetch(`${API}/withdraw`, 
    {
        method: "POST", // clarifies a post request
        headers: { "Content-Type": "application/json" }, // Tells the api that the data is JSON
        body: JSON.stringify(
          { 
            "user_id": userID, 
            "amount": amount
          }
        ) // converst JS object to JSON string(opposite of res.json())
    });

  return validateResponse(res, "Withdraw failed");
}

export const transfer = async (senderID, receiverID, amount) => {
  const res = await fetch(`${API}/transfer`,
  {
    method: "POST",
    headers: { "Content-Type": "application/json" }, // Tells the api that the data is JSON
    body: JSON.stringify(
      {
        "sender_id": senderID, 
        "receiver_id": receiverID, 
        "transaction_amount": amount
      }
    )
  });

  return validateResponse(res, "Transfer failed");
}