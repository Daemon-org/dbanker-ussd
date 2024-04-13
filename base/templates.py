non_users = {
  "n1":{
      "body":"Welcome to DBanker USSD\n1. Register\n2. About Us\n3. Contact Us\n4. Exit",
      "level": 1,
      "part":1,
      "next": "n2",
  },
  "n2": {
      "body":"Enter your email address",
      "level": 2,
      "part":1,
      "next":"n3",
      "back":"n1",
   },
  "n3": {
      "body":"Enter pin code",
      "level":3,
      "part":1,
      "next":"n4",
      "back":"n2",
      "error": "pin must contain only numbers",
   },
  "n4": {
      "body":"Confirm pin code ",
      "level":3,
      "part":2,
      "next":"r1",
      "back":"n3",
      "error": "pin must contain only numbers",
  },
  "n5": {
      "body":"About Us:\nDBanker is a leading bank committed to providing innovative financial solutions to our customers.",
      "level":3,
      "part":2,
      "next":"n1",
      "back":"n1",
  },
  "n6": {
      "body":"Contact Us:\nFor any inquiries or assistance, please contact our customer support at support@dbanker.com",
      "level":3,
      "part":3,
      "next":"n1",
      "back":"n1",
  }
}


registered_users = {
    "r1": {
        "body": "Welcome to DBanker USSD\n1. Send Cash\n2. Deposit Cash \n3. Withdraw Cash\n4. About Us\n5. Contact Us\n6. Exit",
        "level": 1,
        "next": "n2",
    },
    "r2": {
        "body": "About Us:\nDBanker is a leading bank committed to providing innovative financial solutions to our customers.",
        "level": 2,
        "next": "r1",
    },
    "r3": {
        "body": "Contact Us:\nFor any inquiries or assistance, please contact our customer support at support@dbanker.com",
        "level": 3,
        "next": "r1",
    },
    "n2": {
        "body": "Enter recipient's phone number",
        "level": 2,
        "part": 1,
        "next": "n3",
        "back": "r1",
    },
    "n3": {
        "body": "Enter amount to send",
        "level": 2,
        "part": 2,
        "next": "n4",
        "back": "n2",
    },

    "n4": {
        "body": "Confirm transaction: for recipient {} for amount {} GHS \n1. Yes\n2. No",
        "level": 2,
        "part": 3,
        "next": "r1",
        "back": "n3",
    },
    "d2": {
        "body": "Enter amount to deposit",
        "level": 2,
        "part": 1,
        "next": "d3",
        "back": "r1",
    },
    "d3": {
        "body": "Confirm deposit:\n1. Yes\n2. No",
        "level": 2,
        "part": 2,
        "next": "r1",
        "back": "d2",
    },
    "w2": {
        "body": "Enter amount to withdraw",
        "level": 2,
        "part": 1,
        "next": "w3",
        "back": "r1",
    },
    "w3": {
        "body": "Confirm withdrawal:\n1. Yes\n2. No",
        "level": 2,
        "part": 2,
        "next": "r1",
        "back": "w2",
    },
}


guides = {
      "body":"",
      "level":"",
      "part":"",
      "next":"",
   }