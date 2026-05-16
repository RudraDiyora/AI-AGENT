import { useState } from "react";
import { login } from "../api/api";

export default function LoginForm({ setToken, loadUser }) {
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
        loadUser();
        console.log("TOKENNNN", data.access_token);

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
      <div className="form-group">
        <label className="form-label">Email Address</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          onKeyDown={(e) => e.key === "Enter" && handleLogin()}
        />
      </div>
 
      <div className="form-group">
        <label className="form-label">Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
          onKeyDown={(e) => e.key === "Enter" && handleLogin()}
        />
      </div>
 
      <div className="form-actions">
        <button onClick={handleLogin} disabled={loading} style={{ width: "100%" }}>
          {loading ? <><span className="spinner" /> &nbsp;Authenticating…</> : "Sign In"}
        </button>
      </div>
 
      {status && (
        <p className={`status ${isError ? "error" : "success"}`}>
          {isError ? "✗" : "✓"} {status}
        </p>
      )}
    </div>
  );
}