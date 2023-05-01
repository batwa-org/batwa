// function notify(button) {
//     console.log("notify was called here. pls pls chal jao yaar")
//     if (!("Notification" in window)) {
//       alert("This browser does not support desktop notification");
//     } else {
//       Notification.requestPermission().then(function (permission) {
//         if (permission === "granted") {
//           console.log("permission was granted for notifications")
//           try {
//             const text = "We can do it in js";
//             const notification = new Notification("To shehryaar", { body: text });
//           } catch (error) {
//             console.error(error);
//           }
//         }
//       });
//     }
//   }




// function notify(button) {
//     const amount = button.getAttribute("data-amount")
//     console.log("notify was called here. pls pls chal jao yaar m wk")
//     if (Notification.permission !== "granted") {
//       Notification.requestPermission();
//     }
    
//     function showNotification() {
//       const text = "Amount kam h!! ";
//       console.log("Working ")
//       const notification = new Notification("Your balance!", { body: text });
//     }

//     if (amount<=0){
//     setInterval(showNotification, 5000);}}

 



function toggleNotifications(value, frequency = 0) {
  const totalAmount = document.querySelector('h2[data-total-amount]').dataset.totalAmount;
  if (value === "1") {
    
          notify(true, totalAmount, frequency);
       
    } 
    
  else {
    notify(false);
  }
}

function showNotification() {
        const text = "LOW BALANCE!! ";
        const notification = new Notification("Your balance!", { body: text });
      }

let intervalId;

function notify(isEnabled, amount = 1, frequency = 0) {
  if (isEnabled && amount <= 0) {
    if (frequency != 0) {
      intervalId = setInterval(showNotification, frequency * 1000);
    } else {
      stopNotification()
      const text = "Your balance is too low!! Amount =" + amount;
      const notification = new Notification("To do list", { body: text });
    }
  }
  else{stopNotification()}
}

function stopNotification() {
  clearInterval(intervalId);
}



