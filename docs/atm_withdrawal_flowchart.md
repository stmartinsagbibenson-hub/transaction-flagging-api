1. firstly 
2. The API receives a transaction.
3. Validate the transaction.
4. If the transaction is invalid, return a validation error.
5. If valid, check the transaction currency.
6. If the currency is not NGN, get the exchange rate and convert the amount to NGN.
7. Retrieve the account's recent withdrawal history.
8. Check the transaction against all risk rules:
   - Large amount.
   - Rapid withdrawals.
   - Very fast withdrawals.
   - Two large withdrawals within 10 seconds.
   - Cumulative withdrawal limit.
   - Unusual transaction hours.
9. Record any risk flags.
10. Determine the transaction's risk level.
11. If it is a withdrawal, update the account's withdrawal history.
12. Prepare and return the evaluation result.
13. End.
2. Batch Transaction Flowchart
1. Start.
2. The API receives a list of transactions.
3. Prepare an empty results list.
4. Validate each transaction.
5. If a transaction is invalid, record its validation error.
6. If valid, add it to the list of valid transactions.
7. Repeat until all transactions have been checked.
8. Sort valid transactions by timestamp.
9. Evaluate each valid transaction using the risk rules.
10. Store each evaluation result.
11. Arrange the results in their original input order.
12. Calculate the total, successful and failed transactions.
13. Return the batch results and summary.
14. and thats all 