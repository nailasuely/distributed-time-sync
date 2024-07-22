import React from 'react';
import './assets/css/styles.css';
import DigitalClock from './DigitalClock';
import RecentProjects from './components/ContainerClocks'; 
import Footer from './components/Footer'; 

function App() {
  return (
    <div>
      <Footer  />
      <div className="py-20">
      <DigitalClock />
      </div>
      <RecentProjects/> 
      
    </div>
    
  );
}

export default App;
