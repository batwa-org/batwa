function notify() {
    console.log("notify was called here. pls pls chal jao yaar")
    if (!("Notification" in window)) {
      alert("This browser does not support desktop notification");
    } else {
      Notification.requestPermission().then(function (permission) {
        if (permission === "granted") {
          console.log("permission was granted for notifications")
          try {
            const text = "We can do it in js";
            const notification = new Notification("To shehryaar", { body: text });
          } catch (error) {
            console.error(error);
          }
        }
      });
    }
  }