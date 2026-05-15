import { useState } from "react";
import { login } from "../api/api";

export default function LoginForm({ setUser }) {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  const handleLogin = async () => {

    if (!email.includes('@')) {
        setStatus("Invalid email");
        setIsError(true)
        return;
    }

    try {
        setLoading(true);
        setStatus("Processing...");

        const data = await login(email);
        console.log(data);
        localStorage.setItem("user", JSON.stringify(data));
        setUser(data);

        setStatus("Login successful");
        setIsError(false);
    } 
    catch (err) {
        console.log(err);
        setStatus("Login failed");
        setIsError(true);
    } 
    finally {
        setLoading(false);
    }
  };

  return (
    <div>
      <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
      />

      <button onClick={handleLogin} disabled={loading}>
            {loading ? "Processing..." : "Login"}
      </button>


      {status && (
        <p style={{ color: isError ? "red" : "green" }}>
            {status}
        </p>
      )}
    </div>
  );
}