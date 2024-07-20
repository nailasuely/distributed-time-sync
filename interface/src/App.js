import React from 'react';
import './assets/css/styles.css';
import DigitalClock from './DigitalClock';
import RecentProjects from './components/ContainerClocks'; 

function App() {
  return (
    <div>
      <RecentProjects/>
      <DigitalClock />
    </div>
  );
}

export default App;
