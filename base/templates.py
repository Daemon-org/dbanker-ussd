non_users = {
    "n1": {
        "body": "Welcome to DBanker USSD\n1. Register\n2. About Us\n3. Contact Us\n4. Exit",
        "status": 1,
        "next": "n2",
    },
    "n2": {
        "body": "Enter your email address",
        "status": 1,
        "next": "n3",
        "back": "n1",
    },
    "n3": {
        "body": "Enter pin code",
        "status": 1,
        "next": "n4",
        "back": "n2",
        "error": "pin must contain only numbers",
    },
    "n4": {
        "body": "Confirm pin code ",
        "status": 1,
        "next": "r1",
        "back": "n3",
        "error": "pin must contain only numbers",
    },
    "n5": {
        "body": "DBanker is a leading bank committed to providing innovative financial solutions to our customers.\n 1. Back",
        "status": 1,
        "next": "n1",
        "back": "n1",
    },
    "n6": {
        "body": "For any inquiries or assistance, please contact our customer support at support@dbanker.com \n 1. Back",
        "status": 1,
        "next": "n1",
        "back": "n1",
    },
}


registered_users = {
    "r1": {
        "body": "Welcome to DBanker USSD\n1. Send Cash\n2. Deposit Cash \n3. Withdraw Cash\n4. view Statements\n5. Exit",
        "status": 1,
        "next": "n2",
    },
    "r2": {
        "body": "About Us:\nDBanker is a leading bank committed to providing innovative financial solutions to our customers.",
        "status": 1,
        "next": "r1",
    },
    "r3": {
        "body": "Contact Us:\nFor any inquiries or assistance, please contact our customer support at support@dbanker.com",
        "status": 1,
        "next": "r1",
    },
    "s2": {
        "body": "Enter recipient's phone number",
        "status": 1,
        "part": 1,
        "next": "n3",
        "back": "r1",
    },
    "s3": {
        "body": "Enter amount to send",
        "status": 1,
        "part": 2,
        "next": "n4",
        "back": "n2",
    },
    "s4": {
        "body": "Confirm transaction: for recipient {} for amount {} GHS \n1. Enter Code\n2. Cancel",
        "status": 1,
        "part": 3,
        "next": "xp",
        "back": "n3",
        "error": "Unable to send funds",
        "error2":"Insufficient funds"
    },
    "d2": {
        "body": "Enter amount to deposit",
        "status": 1,
        "part": 1,
        "next": "d3",
        "back": "r1",
    },
    "d3": {
        "body": "Confirm deposit: for amount {} GHS\n1. Yes\n2. Cancel",
        "status": 1,
        "part": 2,
        "next": "r1",
        "back": "d2",
    },
    "w2": {
        "body": "Enter amount to withdraw",
        "status": 1,
        "part": 1,
        "next": "w3",
        "back": "r1",
    },
    "w3": {
        "body": "Confirm withdrawal for {} GHS \n1. Enter Code\n2. No",
        "status": 1,
        "part": 2,
        "next": "r1",
        "back": "w2",
    },
    "x1": {
        "body": "Your trasaction staetment for the past week will be sent to you via sms. Thank you for using DBanker"
        + "\n1. Exit",
        "status": 1,
    },
    "xp":{
        "body":"Enter your pin to confirm transaction",
        "status":2,
        "error1":"Incorrect Pin",
        "error2": "It seems you've submitted an invalid pin code. You have {} more tries",
        "error3": "you have exceeded the number of pin entries try again later",
    },
    "dp":{
        "body":"Enter your pin to confirm transaction",
        "status":2,
        "error1":"Incorrect Pin",
        "error2": "It seems you've submitted an invalid pin code. You have {} more tries",
        "error3": "you have exceeded the number of pin entries try again later",
    }
}


guides = {
    "body": "",
    "status": 1,
    "part": "",
    "next": "",
}
