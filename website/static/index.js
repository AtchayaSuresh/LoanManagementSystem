function deleteBorrower(borrowerId) {
  fetch("/delete-borrower", {
    method: "POST",
    body: JSON.stringify({ borrowerId: borrowerId }),
  }).then((_res) => {
    window.location.href = "/borrowers-list";
  });
}

function deleteTransaction(transactionId, userId) {
  console.log(transactionId);
  fetch("/delete-transaction", {
    method: "POST",
    body: JSON.stringify({ transactionId: transactionId, userId: userId }),
  }).then((_res) => {
    window.location.href = "/transactions-list?user=" + userId;
  });
}
