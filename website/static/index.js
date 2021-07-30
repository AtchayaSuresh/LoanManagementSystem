function deleteBorrower(borrowerId) {
  fetch("/delete-borrower", {
    method: "POST",
    body: JSON.stringify({ borrowerId: borrowerId }),
  }).then((_res) => {
    window.location.href = "/borrowers-list";
  });
}

function deleteTransaction(transactionId, borrowerId, lenderId) {
  console.log(transactionId);
  fetch("/delete-transaction", {
    method: "POST",
    body: JSON.stringify({ transactionId: transactionId, borrowerId: borrowerId, lenderId: lenderId }),
  }).then((_res) => {
    window.location.href = "/transactions-list?borrower=" + borrowerId +"&lender="+lenderId;
  });
}
