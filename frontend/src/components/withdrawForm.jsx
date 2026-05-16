import { useState } from "react";
import { withdraw } from "../api/api";

export default function WithdrawForm({}) {
  const [amount, setAmount] = useState("");
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isError, setIsError] = useState(false);


  const handleWithdraw = async () => {
    const numericAmount = parseFloat(amount);

    if (isNaN(numericAmount) || numericAmount <= 0) {
        setStatus("Invalid amount");
        setIsError(true);
        return;
    }

    try {
        setLoading(true);
        setStatus("Processing...");

        await withdraw(numericAmount);

        setStatus("Withdraw successful");
        setAmount("");
        setIsError(false);
    } 
    catch (err) {
        alert(err);
        setStatus("Withdraw failed");
        setIsError(true);
    } 
    finally {
        setLoading(false);
    }
  };

  return (
    <div>
      <div className="form-group">
        <label className="form-label">Amount (USD)</label>
        <input
          type="number"
          step="0.01"
          min="0"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          placeholder="0.00"
          onKeyDown={(e) => e.key === "Enter" && handleWithdraw()}
        />
      </div>
 
      <div className="form-actions">
        <button onClick={handleWithdraw} disabled={loading} style={{ width: "100%" }}>
          {loading ? <><span className="spinner" /> &nbsp;Processing…</> : "Withdraw Funds"}
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