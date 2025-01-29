// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import {getAuth} from 'firebase/auth'

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyA9CBUJ4kFtg7WV-mjP3qoLK2CKvZNB8M4",
  authDomain: "fileshare-2553f.firebaseapp.com",
  projectId: "fileshare-2553f",
  storageBucket: "fileshare-2553f.firebasestorage.app",
  messagingSenderId: "261118256232",
  appId: "1:261118256232:web:d8dabcce1db0c45d41c7dd",
  measurementId: "G-KPVPS4TE89"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);

export { app, auth };