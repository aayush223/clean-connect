// Firebase Configuration
const firebaseConfig = {
  apiKey: "AIzaSyCHduj3dyE03oxPT3ES1QFiyqq-qSkp8XI",
  authDomain: "clean-connect-32d5c.firebaseapp.com",
  projectId: "clean-connect-32d5c",
  storageBucket: "clean-connect-32d5c.firebasestorage.app",
  messagingSenderId: "859887619622",
  appId: "1:859887619622:web:3ce4455505b5f762c4e0e7",
  measurementId: "G-Y9GRCNLR9K"
};

// Initialize Firebase
let messaging = null;
try {
    firebase.initializeApp(firebaseConfig);
    messaging = firebase.messaging();
    
    messaging.onMessage((payload) => {
        console.log('Foreground FCM Message received. ', payload);
        alert(`🚨 FCM Alert: ${payload.notification.title}\n${payload.notification.body}`);
    });
} catch (e) {
    console.error("Firebase FCM init failed. Check secure context or config.", e);
}

function requestNotificationPermission() {
    if (!("Notification" in window)) return;
    Notification.requestPermission().then((permission) => {
        if (permission === 'granted') {
            console.log('FCM Notification permission granted.');
            // In a real app we would call messaging.getToken({ vapidKey: '...' }) here
        }
    });
}

let currentRole = '';
const MAP_API_KEY = 'uaemqmrsfcygejzbgqodgtkwmkmthiytdgtt';
let maps = {};

function initMap(mapId) {
    if (maps[mapId]) {
        maps[mapId].invalidateSize();
        return;
    }
    
    const map = L.map(mapId).setView([28.6139, 77.2090], 12);
    
    // The provided MapmyIndia API key returns HTTP 401 Unauthorized. 
    // Falling back to CartoDB Dark Matter tiles which also fit the UI perfectly.
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap contributors, © CARTO'
    }).addTo(map);
    
    maps[mapId] = map;
    
    if(mapId === 'citizenMap' || mapId === 'adminMap') {
        const binIcon = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
        });
        const redIcon = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
        });
        
        L.marker([28.6139, 77.2090], {icon: binIcon}).addTo(map).bindPopup('<b>Smart Bin A1</b><br>20% Full');
        L.marker([28.6239, 77.2190], {icon: redIcon}).addTo(map).bindPopup('<b>Smart Bin B2</b><br>95% Full (Overflow Risk)');
        L.marker([28.6050, 77.1990], {icon: redIcon}).addTo(map).bindPopup('<b>Citizen Report</b><br>SLA Deadline: 22 Hrs left');
    } else if (mapId === 'workerMap') {
        const truckIcon = L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34], shadowSize: [41, 41]
        });
        L.marker([28.6139, 77.2090], {icon: truckIcon}).addTo(map).bindPopup('<b>Your Location</b>');
        L.marker([28.6050, 77.1990]).addTo(map).bindPopup('<b>Active Task</b><br>Clean garbage pile');
        L.polyline([[28.6139, 77.2090], [28.6100, 77.2050], [28.6050, 77.1990]], {color: '#00F2FE', weight: 4}).addTo(map);
    }
}

function showAppPortal(role) {
    document.getElementById('citizenPortal').style.display = 'none';
    document.getElementById('workerPortal').style.display = 'none';
    document.getElementById('adminPortal').style.display = 'none';
    document.querySelector('.landing-content').style.display = 'none';
    
    const portalId = role.toLowerCase() + 'Portal';
    const mapId = role.toLowerCase() + 'Map';
    
    const portalEl = document.getElementById(portalId);
    if(portalEl) {
        portalEl.style.display = 'block';
        setTimeout(() => {
            initMap(mapId);
            
            // Push Notification & Service Worker Logic for Sanitation Worker
            if (role.toLowerCase() === 'worker') {
                requestNotificationPermission();
                
                // Simulate an incoming FCM push notification 3.5 seconds after login
                setTimeout(() => {
                    const title = "🚨 Urgent SLA Task Assigned";
                    const options = { body: "Citizen reported a garbage pile 2.4km away. 36-hr SLA active." };
                    
                    if (Notification.permission === 'granted') {
                        new Notification(title, options);
                    } else {
                        // Fallback to JS Alert if native notifications are blocked
                        alert(`FCM Push Simulation:\n${title}\n${options.body}`);
                    }
                }, 3500);
            }
        }, 300);
    }
}

function closeAppPortal() {
    document.getElementById('citizenPortal').style.display = 'none';
    document.getElementById('workerPortal').style.display = 'none';
    document.getElementById('adminPortal').style.display = 'none';
    document.querySelector('.landing-content').style.display = 'block';
}

function openPortal(role) {
    currentRole = role.toUpperCase();
    const modal = document.getElementById('portalModal');
    const title = document.getElementById('modalTitle');
    const authStatus = document.getElementById('authStatus');
    
    let roleTitle = 'Portal Access';
    if(role === 'citizen') roleTitle = 'Citizen PWA Authentication';
    if(role === 'worker') roleTitle = 'Worker PWA Authentication';
    if(role === 'admin') roleTitle = 'Admin System Login';
    
    title.innerText = roleTitle;
    authStatus.innerText = '';
    authStatus.style.color = '';
    document.getElementById('authForm').reset();
    
    modal.style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('portalModal');
    modal.style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('portalModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

document.getElementById('authForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const statusMsg = document.getElementById('authStatus');
    statusMsg.style.color = 'var(--primary)';
    statusMsg.innerText = 'Authenticating and initializing PWA constraints...';
    
    setTimeout(async () => {
        try {
            statusMsg.innerText = `Fetching ${currentRole} scoped manifest...`;
            
            statusMsg.style.color = 'var(--accent-dark)';
            statusMsg.innerHTML = `Authentication Successful.<br>Installing <b>${currentRole}</b> specific PWA features...`;
            
            setTimeout(() => {
                closeModal();
                showAppPortal(currentRole);
            }, 1000);

        } catch (error) {
            statusMsg.style.color = '#ff4b4b';
            statusMsg.innerText = 'Authentication failed. Please check backend connection.';
        }
    }, 1000);
});
