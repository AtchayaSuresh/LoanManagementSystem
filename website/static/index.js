// const signUpButton = document.getElementById('signUp');
// const signInButton = document.getElementById('signIn');
// const container = document.getElementById('container');

// signUpButton.addEventListener('click', () => {
//   console.log("dg");
// 	container.classList.add("right-panel-active");
//     //alert("fs");
// });

// signInButton.addEventListener('click', () => {
// 	container.classList.remove("right-panel-active");
// });


function deleteBorrower(borrowerId) {
  fetch("/delete-borrower", {
    method: "POST",
    body: JSON.stringify({ borrowerId: borrowerId }),
  }).then((_res) => {
    window.location.href = "/borrowers-list";
  });
}

function deleteTransaction(transactionId,userId) {
  console.log(transactionId);
  fetch("/delete-transaction", {
    method: "POST",
    body: JSON.stringify({ transactionId: transactionId, userId: userId }),
  }).then((_res) => {
    window.location.href = "/transactions-list?user="+userId;
  });
}