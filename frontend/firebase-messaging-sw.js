importScripts('https://www.gstatic.com/firebasejs/10.4.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.4.0/firebase-messaging-compat.js');

const firebaseConfig = {
  apiKey: "AIzaSyCHduj3dyE03oxPT3ES1QFiyqq-qSkp8XI",
  authDomain: "clean-connect-32d5c.firebaseapp.com",
  projectId: "clean-connect-32d5c",
  storageBucket: "clean-connect-32d5c.firebasestorage.app",
  messagingSenderId: "859887619622",
  appId: "1:859887619622:web:3ce4455505b5f762c4e0e7",
  measurementId: "G-Y9GRCNLR9K"
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/assets/icon-192.png'
    };
    self.registration.showNotification(notificationTitle, notificationOptions);
});
