import { useState } from "react";
import { login } from "../api/api";

export default function LoginForm({ setToken, setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
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

        const data = await login(email, password);

        localStorage.setItem("token", data.access_token);
        setToken(data.access_token);

        setUser({
          user_id: data.user_id,
          email: data.email,
          name: data.name
        });

        setStatus("Login successful");
        setIsError(false);
    } 
    catch (err) {
        console.log(err);
        setStatus("Login failed");
        setIsError(true);
    } 
    finally {
        setEmail("");
        setPassword("");
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
      <input
            type="text"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
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