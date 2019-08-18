// Usage: node get_subcollections.js (Path to Firebase Credentials) (Path to Document separated with '/')
// Example: node get_subcollections.js ./secret.json EDMC/_test

cred_file = process.argv[2];
doc_path = process.argv[3];

const admin = require('firebase-admin');

let serviceAccount = require(cred_file);

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

let db = admin.firestore();

let sfRef = db.doc(doc_path);
sfRef.listCollections().then(collections => {
    collections.forEach((collection, index, collections) => {
        collections[index] = collection.id;
    });
    console.log(collections.toString())
});
