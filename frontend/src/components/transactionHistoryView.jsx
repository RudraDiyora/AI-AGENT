import { useState } from "react";
import { getTransactionHistory } from "../api/api";

export default function TransactionHistoryView ({}) {
    const [transactionHistory, setTransactionHistory] = useState([]);
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(false);
    const [isError, setIsError] = useState(false);
    const [fetched, setFetched] = useState(false);

    const handleTransactionHistoryRetrieval = async() => {
        try {
            setLoading(true);
            setStatus("Processing...");

            // attempt a retrieval and update the state-value
            const transactionHistory_ = await getTransactionHistory();
            setTransactionHistory(transactionHistory_);
            
            setStatus("Transaction History retrieval successful");
            setFetched(true);
            setIsError(false);
        } catch(err) {
            console.log(err);
            setStatus("Transaction History retrieval FAILED")
            setFetched(false);
            setIsError(true);
        } finally {
            setLoading(false);
        }
    };

    const getBadgeClass = (type) => {
        if (!type) return "";
        const t = type.toLowerCase();
        if (t.includes("deposit")) return "deposit";
        else if (t.includes("withdraw")) return "withdraw";
        else if (t.includes("transfer")) return "transfer";
        return "";
    };


    return (
    <div>
        <div style={{ padding: "28px 24px", display: "flex", alignItems: "center", gap: 12 }}>
            <button onClick={handleTransactionHistoryRetrieval} disabled={loading} className="ghost" style={{ padding: "10px 20px" }}>
            {loading ? <><span className="spinner" style={{ borderTopColor: "var(--gold)", borderColor: "var(--border)" }} /> &nbsp;Loading…</> : fetched ? "Refresh" : "Load History"}
            </button>
    
            {status && (
            <p className={`status ${isError ? "error" : "success"}`} style={{ margin: 0 }}>
                {isError ? "✗" : "✓"} {status}
            </p>
            )}
        </div>
    
        {fetched && (
            transactionHistory.length === 0 ? (
            <p className="tx-empty">No transactions found.</p>
            ) : (
            <div style={{ overflowX: "auto" }}>
                <table className="tx-table">
                <thead>
                    <tr>
                    <th>ID</th>
                    <th>From</th>
                    <th>To</th>
                    <th>Amount</th>
                    <th>Type</th>
                    </tr>
                </thead>
                <tbody>
                    {transactionHistory.map((tx, i) => (
                    <tr key={tx.id ?? i} style={{ animationDelay: `${i * 40}ms` }}>
                        <td className="tx-id">#{tx.id}</td>
                        <td>{tx.sender_id ?? "—"}</td>
                        <td>{tx.receiver_id ?? "—"}</td>
                        <td className="tx-amount">
                        ${parseFloat(tx.amount).toFixed(2)}
                        </td>
                        <td>
                        <span className={`tx-type-badge ${getBadgeClass(tx.type)}`}>
                            {tx.type}
                        </span>
                        </td>
                    </tr>
                    ))}
                </tbody>
                </table>
            </div>
            )
        )}
    </div>
    );
}