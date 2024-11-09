// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDc0_25AKc01rh5CD-9hiV1GvXYofcxmCY",
  authDomain: "book2ball-6687d.firebaseapp.com",
  projectId: "book2ball-6687d",
  storageBucket: "book2ball-6687d.firebasestorage.app",
  messagingSenderId: "822066502925",
  appId: "1:822066502925:web:fbaefa30872658cc05a444",
  measurementId: "G-DW9FLY7NPC"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const analytics = getAnalytics(app);

export { auth, analytics };