import { useState } from "react";
import { deposit } from "../api/api";

export default function DepositForm({ userID }) {
  const [amount, setAmount] = useState("");
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  const handleDeposit = async () => {
    const numericAmount = parseFloat(amount);

    if (isNaN(numericAmount) || numericAmount <= 0) {
        setStatus("Invalid amount");
        setIsError(true)
        return;
    }

    try {
        setLoading(true);
        setStatus("Processing...");

        await deposit(userID, numericAmount);

        setStatus("Deposit successful");
        setAmount("");
        setIsError(false);
    } 
    catch (err) {
        alert(err);
        setStatus("Deposit failed");
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
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="Amount"
      />

      <button onClick={handleDeposit} disabled={loading}>
            {loading ? "Processing..." : "Deposit"}
      </button>


      {status && (
        <p style={{ color: isError ? "red" : "green" }}>
            {status}
        </p>
      )}
    </div>
  );
}