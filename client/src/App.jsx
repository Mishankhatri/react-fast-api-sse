import { useEffect, useState } from "react";
import { v4 as uuid } from "uuid";
import "./App.css";
import getNotificationsApi from "./services/getNotifications.api";

function App() {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/stream");
    eventSource.onopen = (event) => {
      console.log("SSE stream opened successfully.");
    };

    eventSource.onmessage = (event) => {
      setNotifications((prev) => [...prev, JSON.parse(event.data)?.data]);
    };

    return () => {
      eventSource.close();
    };
  }, []);

  useEffect(() => {
    const getNotifications = async () => {
      const results = await getNotificationsApi();
      if (results) {
        setNotifications(results?.data);
      }
    };
    getNotifications();
  }, []);

  return (
    <div>
      <h1>Notice Board - SSE </h1>
      <div className="notice-container">
        {notifications.length === 0 && <h3>No notifications found.</h3>}
        {notifications.map((notification) => {
          return (
            <div key={uuid()} className="notice-card">
              <h3>{notification.name}</h3>
              <p>{notification.description}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default App;
