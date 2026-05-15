import { useState } from "react";
import { getTransactionHistory } from "../api/api";

export default function TransactionHistoryView ({userID}) {
    const [transactionHistory, setTransactionHistory] = useState([]);
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(false);
    const [isError, setIsError] = useState(false);

    const handleTransactionHistoryRetrieval = async() => {
        try {
            setLoading(true);
            setStatus("Processing...");

            // attempt a retrieval and update the state-value
            const transactionHistory_ = await getTransactionHistory(userID);
            setTransactionHistory(transactionHistory_);
            
            setStatus("Transaction History retrieval successful");
            setIsError(false);
        } catch(err) {
            console.log(err);
            setStatus("Transaction History retrieval FAILED")
            setIsError(true);
        } finally {
            setLoading(false);
        }
    };


    return (
        <div>
            <button onClick={handleTransactionHistoryRetrieval} disabled={loading}>
                 {loading ? "Processing..." : "Get Transaction History"}
            </button>
            {status && (
                <p style={{ color: isError ? "red" : "green" }}>
                    {status}
                </p>
            )} 

            {
                (status == "Transaction History retrieval successful") ?
                transactionHistory.map(transaction => (
                    <div key={transaction.id}>
                        <div> From: {transaction.sender_id} </div>
                        <div> To: {transaction.receiver_id} </div>
                        <div> Amount: {transaction.amount} </div>
                        <div> Type: {transaction.type} </div>
                    </div>
                ))
                : ""
            }

        </div>
    );
}