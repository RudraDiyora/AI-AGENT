import { useState } from "react";
import { transfer } from "../api/api";

export default function TransferForm({ userID }) {
  const [amount, setAmount] = useState("");
  const [receiverID, setReceiverID] = useState("")
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isError, setIsError] = useState(false);


  const handleTransfer = async () => {
    const numericAmount = parseFloat(amount);

    if (!receiverID) {
        setStatus("Receiver ID is required");
        setIsError(true);
        return;
    }

    if (isNaN(numericAmount) || numericAmount <= 0) {
        setStatus("Invalid amount");
        setIsError(true);
        return;
    }

    try {
        setLoading(true);
        setStatus("Processing...");

        await transfer(userID, receiverID, numericAmount);

        // Reset all the fields
        setStatus("Transfer successful");
        setAmount("");
        setReceiverID("");
        setIsError(false);
    } 
    catch (err) {
        alert(err);
        setStatus("Transfer failed");
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
            value={receiverID}
            onChange={(e) => setReceiverID(e.target.value)}
            placeholder="Receiver ID"
      />

      <input
            type="number"
            step="0.01"
            min="0"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            placeholder="Amount"
      />

      <button onClick={handleTransfer} disabled={loading}>
            {loading ? "Processing..." : "Transfer"}
      </button>

      {status && (
        <p style={{ color: isError ? "red" : "green" }}>
            {status}
        </p>
      )}
    </div>
  );
}