TRANSACTION EVALUATION
To begin, the API will receive a transaction from the user and validate the transaction.
If the transaction is invalid, the API will return a validation error.
If the transaction is valid, the API will read the transaction amount and currency.
If the currency is not NGN, the API will request the exchange rate and convert the transaction amount to Naira.
If the exchange rate is unavailable, the API will return an exchange rate error.
Next, the API will retrieve the account's recent withdrawal history.
The API will check if the withdrawal amount is unusually large, if withdrawals are happening rapidly, if multiple withdrawals are happening within a very short period, if repeated large withdrawals are occurring, and if the cumulative withdrawal limit has been exceeded.
The API will also check if the transaction was made during unusual hours.
After checking all the rules, the API will record the triggered risk flags and determine the transaction's risk level.
If the transaction is a withdrawal, the API will update the account's withdrawal history.
Finally, the API will return the transaction evaluation result, including the risk level and any triggered risk flags.

BATCH EVALUATION

To begin, the API will receive a list of transactions from the user and prepare an empty results list.

The API will validate each transaction in the list.

If a transaction is invalid, the API will record the validation error and continue to the next transaction.

If a transaction is valid, the API will add it to the list of valid transactions.

After validating all transactions, the API will arrange the valid transactions according to their timestamps, starting with the earliest.

Next, the API will evaluate each valid transaction and add its evaluation result to the results list.

After evaluating all valid transactions, the API will arrange the results in their original input order.

Finally, the API will calculate the total number of transactions, successful evaluations, and failed evaluations before returning the batch results and summary.

