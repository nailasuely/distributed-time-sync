import React, { useEffect, useState } from 'react';
import '../assets/css/styles.css';

function Clock({ apiUrl }) {
  const [time, setTime] = useState({
    hour: '',
    minutes: '',
    seconds: '',
    day: '',
  });

  const convertSecondsToTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return {
      hour: String(hours).padStart(2, '0'),
      minutes: String(minutes).padStart(2, '0'),
      seconds: String(secs).padStart(2, '0')
    };
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        const leaderValueInSeconds = data.leader_value;
        
        const { hour, minutes, seconds } = convertSecondsToTime(leaderValueInSeconds);
        const now = new Date();
        setTime({
          hour,
          minutes,
          seconds,
          day: `${now.getDate()}/${now.getMonth() + 1}/${now.getFullYear()}`
        });
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 1000);
    

    return () => clearInterval(interval);
  }, [apiUrl]);

  return (
    <div className="box">
      <div className="clock">
        <div className="front-clock">
          <div id="hour">{time.hour}</div>
          <p>hour</p>
        </div>
      </div>
      <div className="clock">
        <div className="front-clock">
          <div id="minute">{time.minutes}</div>
          <p>minute</p>
        </div>
      </div>
      <div className="clock">
        <div className="front-clock">
          <div id="seconds">{time.seconds}</div>
          <p>seconds</p>
        </div>
      </div>
    </div>
  );
}

export default Clock;
