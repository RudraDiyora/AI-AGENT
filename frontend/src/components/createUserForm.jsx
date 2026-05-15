import { useState } from "react";
import { createUser } from "../api/api";

export default function CreateUserForm() {
  const [userName, setUserName] = useState("");
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  const handleUserCreate = async () => {
    try {
        setLoading(true);
        setStatus("Processing...");

        await createUser(userName, email, password);

        setStatus("User successfully created");

        // Reset all the input fields
        setUserName("");
        setEmail("");
        setPassword("");
        setIsError(false);
    } 
    catch (err) {
        alert(err);
        setStatus("User creation failed");
        setIsError(true);
    } 
    finally {
        setLoading(false);
    }

  };

  return (
    <div>
      <input
            type="text"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
            placeholder="Name"
      />
      <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
      />
      <input
            type="text"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
      />


      <button onClick={handleUserCreate} disabled={loading}>
            {loading ? "Processing..." : "Create"}
      </button>


      {status && (
        <p style={{ color: isError ? "red" : "green" }}>
            {status}
        </p>
      )}
    </div>
  );
}