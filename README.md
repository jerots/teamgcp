
# Mock iBanking Login

Through an interface that mocks iBanking application login, we developed three proof of concepts for banking authentication through user's keystrokes while typing their user id or pin.


### Prototype 1 (most practical)
1. Learn a user's type pattern through machine learning
2. When the user is typing in their username and password, the application can decide whether the user is an attacker despite entering the correct authentication details

This serves as a 2FA that is different from the usual SMS/hardware token supporting authentication.

### Prototype 2
1. Learn a user's type pattern through machine learning
2. By only entering their user id, we authenticate the user based on their keystroke. No password/pin required.

### Prototype 3 (most idealistic)
1. Learn a user's type pattern through machine learning
2. By typing in a random sentence or phrase, the algorithm can identify and log the user in. No user id or pin required.
