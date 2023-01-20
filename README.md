# MessagingApp
- A Flask API for a simple and secure chat app 
- The API uses both HTTP and WebSockets
- The messages are encrypted in the client then sent to the flask app which serves as a relay and sends them to the destination client where they get decrypted.
- The authentication is done both through an LDAP Server (screenshot below) and a database (MongoDB).

![Screenshot from 2023-01-20 16-46-41](https://user-images.githubusercontent.com/61352133/213742724-becdbf44-919a-48dd-af57-7c64a3a8a828.png)

## Repo of the client app (react)
https://github.com/AlaaCherif/chat-app-front

## Demo
![Screenshot from 2023-01-20 16-29-27](https://user-images.githubusercontent.com/61352133/213738119-6c8c07a3-2139-4dfb-9a14-4263a0aa70ce.png)
![Screenshot from 2023-01-20 16-30-38](https://user-images.githubusercontent.com/61352133/213738230-7be3bab2-7065-480c-967d-bde23f22062d.png)
