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

// Token -> User
export const get_session_user = async(access_token) => {

  if (!access_token) {
    throw new Error("No session token found");
  }
  const res = await fetch(`${API}/me`,
  {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${access_token}`
    }
  });

  return validateResponse(res, "session retrieval failed")
}

// Login
export const login = async(email, password) => {
  console.log(password);
  const res = await fetch(`${API}/login`,
  {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
       },
      body: JSON.stringify(
        {
          "email": email,
          "password": password
        }
      )
  });

  return validateResponse(res, "login failed")
}

// User Views
export const getBalance = async() => {
  const res = await fetch(`${API}/balance`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    }  
});
  return validateResponse(res, "Balance retrieval failed");
}

export const getTransactionHistory = async() => {
  const res = await fetch(`${API}/transaction-history`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    }
  });
  return validateResponse(res, "Transaction history retrieval failed");
}

// User Handeling
export const createUser = async(userName, email, password) => {
    const res = await fetch(`${API}/create-user`, 
    { // because POST/deposit/ takes a "deposite" object, we have to convert the data
        method: "POST", // clarifies a post request
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}` 
        }, // Tells the api that the data is JSON
        body: JSON.stringify(
          { 
            "name": userName, 
            "email": email,
            "password": password,
          }
        ) // converst JS object to JSON string(opposite of res.json())
    });

    return validateResponse(res, "User creation failed");
}

export const deposit = async (amount) => {
    const res = await fetch(`${API}/deposit`, 
    { // because POST/deposit/ takes a "deposite" object, we have to convert the data
        method: "POST", // clarifies a post request
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
         }, // Tells the api that the data is JSON
        body: JSON.stringify(
          { 
            "amount": amount
          }
        ) // converst JS object to JSON string(opposite of res.json())
    });
  return validateResponse(res, "Deposit failed");
}

export const withdraw = async (amount) => {
    const res = await fetch(`${API}/withdraw`, 
    {
        method: "POST", // clarifies a post request
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        }, // Tells the api that the data is JSON
        body: JSON.stringify(
          { 
            "amount": amount
          }
        ) // converst JS object to JSON string(opposite of res.json())
    });

  return validateResponse(res, "Withdraw failed");
}

export const transfer = async (receiverID, amount) => {
  const res = await fetch(`${API}/transfer`,
  {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    }, // Tells the api that the data is JSON
    body: JSON.stringify(
      {
        "receiver_id": receiverID, 
        "transaction_amount": amount
      }
    )
  });

  return validateResponse(res, "Transfer failed");
}

