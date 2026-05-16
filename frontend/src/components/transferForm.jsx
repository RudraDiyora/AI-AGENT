import { useState } from "react";
import { transfer } from "../api/api";

export default function TransferForm({ }) {
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

        await transfer(receiverID, numericAmount);

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
      <div className="form-group">
        <label className="form-label">Recipient ID</label>
        <input
          type="text"
          value={receiverID}
          onChange={(e) => setReceiverID(e.target.value)}
          placeholder="Recipient account ID"
        />
      </div>
 
      <div className="form-group">
        <label className="form-label">Amount (USD)</label>
        <input
          type="number"
          step="0.01"
          min="0"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          placeholder="0.00"
          onKeyDown={(e) => e.key === "Enter" && handleTransfer()}
        />
      </div>
 
      <div className="form-actions">
        <button onClick={handleTransfer} disabled={loading} style={{ width: "100%" }}>
          {loading ? <><span className="spinner" /> &nbsp;Processing…</> : "Send Transfer"}
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