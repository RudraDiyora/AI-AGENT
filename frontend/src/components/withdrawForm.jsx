import { useState } from "react";
import { withdraw } from "../api/api";

export default function WithdrawForm({ userID }) {
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

        await withdraw(userID, numericAmount);

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
      <input
            type="number"
            step="0.01"
            min="0"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="Amount"
      />

      <button onClick={handleWithdraw} disabled={loading}>
            {loading ? "Processing..." : "Withdraw"}
      </button>

      {status && (
        <p style={{ color: isError ? "red" : "green" }}>
            {status}
        </p>
      )}
    </div>
  );
}