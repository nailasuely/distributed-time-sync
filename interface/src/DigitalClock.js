import React, { useEffect, useState } from 'react';
import './assets/css/styles.css';
import { IP } from "./components/IP";

function DigitalClock() {
  const [time, setTime] = useState({
    hour: '',
    minutes: '',
    seconds: '',
    day: '',
  });

  //  converter o valor para horas, minutos e segundos
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
        // atualizar 
        const leaderResponse = await fetch(`http://${IP}/leader`);
        if (!leaderResponse.ok) {
          throw new Error('Network response was not ok');
        }
        const leaderData = await leaderResponse.json();
        const leaderValueInSeconds = leaderData.leader_value;

        //converter aqui 
        const { hour, minutes, seconds } = convertSecondsToTime(leaderValueInSeconds);
        
        // atualizar 
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
  }, []);

  return (
    <main className="container">
    <div className="py-10">
      <h1 className="heading">
      Distributed Time Sync</h1>
      </div>
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
    </main>
  );
}

export default DigitalClock;
