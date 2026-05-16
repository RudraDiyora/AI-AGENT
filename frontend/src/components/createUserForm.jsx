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
      <div className="form-group">
        <label className="form-label">Full Name</label>
        <input
          type="text"
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
          placeholder="Your full name"
        />
      </div>
 
      <div className="form-group">
        <label className="form-label">Email Address</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
        />
      </div>
 
      <div className="form-group">
        <label className="form-label">Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
        />
      </div>
 
      <div className="form-actions">
        <button onClick={handleUserCreate} disabled={loading} style={{ width: "100%" }}>
          {loading ? <><span className="spinner" /> &nbsp;Creating Account…</> : "Open Account"}
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