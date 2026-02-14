// Funcionalidad para el sistema de notificaciones

// WebSocket connection
let notificationSocket;

function connectWebSocket() {
    notificationSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/notifications/'
    );

    notificationSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.type === 'notification') {
            addNotification(data.title, data.body, data.topic);
        }
    };

    notificationSocket.onclose = function(e) {
        console.error('Notification socket closed unexpectedly');
        // Intentar reconectar después de 2 segundos
        setTimeout(connectWebSocket, 2000);
    };

    notificationSocket.onerror = function(e) {
        console.error('WebSocket error:', e);
    };
}

// Iniciar conexión WebSocket
document.addEventListener('DOMContentLoaded', function() {
    connectWebSocket();
    
    // Form submission
    const form = document.getElementById('notification-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const title = document.getElementById('title').value;
            const body = document.getElementById('body').value;
            const topic = document.getElementById('topic').value;
            
            fetch('/api/send-notification/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    title: title,
                    body: body,
                    topic: topic
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('title').value = '';
                    document.getElementById('body').value = '';
                } else {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al enviar la notificación');
            });
        });
    }

    // Load initial notifications
    loadNotifications();
});

function loadNotifications() {
    fetch('/api/notifications/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('notifications-container');
            if (!container) return;
            
            container.innerHTML = '';
            
            if (data.notifications && data.notifications.length > 0) {
                data.notifications.forEach(notification => {
                    addNotificationToDOM(
                        notification.title,
                        notification.body,
                        notification.topic,
                        new Date(notification.created_at)
                    );
                });
            } else {
                container.innerHTML = '<p class="text-center">No hay notificaciones disponibles.</p>';
            }
        })
        .catch(error => {
            console.error('Error loading notifications:', error);
        });
}

function addNotification(title, body, topic) {
    addNotificationToDOM(title, body, topic, new Date());
}

function addNotificationToDOM(title, body, topic, time) {
    const container = document.getElementById('notifications-container');
    if (!container) return;
    
    const notificationDiv = document.createElement('div');
    notificationDiv.className = 'notification bg-light';
    
    const titleElement = document.createElement('div');
    titleElement.className = 'notification-title';
    titleElement.textContent = title;
    
    const bodyElement = document.createElement('div');
    bodyElement.className = 'notification-body';
    bodyElement.textContent = body;
    
    const metaElement = document.createElement('div');
    metaElement.className = 'notification-meta d-flex justify-content-between mt-2';
    
    const topicElement = document.createElement('span');
    topicElement.className = 'badge bg-secondary';
    topicElement.textContent = topic;
    
    const timeElement = document.createElement('span');
    timeElement.className = 'notification-time';
    timeElement.textContent = formatTime(time);
    
    metaElement.appendChild(topicElement);
    metaElement.appendChild(timeElement);
    
    notificationDiv.appendChild(titleElement);
    notificationDiv.appendChild(bodyElement);
    notificationDiv.appendChild(metaElement);
    
    container.prepend(notificationDiv);
}

function formatTime(date) {
    return date.toLocaleTimeString() + ' ' + date.toLocaleDateString();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}