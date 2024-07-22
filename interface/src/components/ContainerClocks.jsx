import React, { useState } from "react";
import { FaLocationArrow } from 'react-icons/fa';
import { projects } from '../data/projects';  
import { PinContainer } from './PinContainer';
import Clock from './Clock';

const apiUrls = [
  'http://localhost:5030/leader',
  'http://localhost:5031/leader',
  'http://localhost:5032/leader'
];

const driftUrls = [
  'http://localhost:5030/drift',
  'http://localhost:5031/drift',
  'http://localhost:5032/drift'
];

const RecentProjects = () => {
  const [driftInputs, setDriftInputs] = useState(apiUrls.map(() => ''));
  const [statusMessages, setStatusMessages] = useState(apiUrls.map(() => ''));

  const handleDriftChange = (index, event) => {
    const newDriftInputs = [...driftInputs];
    newDriftInputs[index] = event.target.value;
    setDriftInputs(newDriftInputs);
  };

  const handleDriftUpdate = async (index) => {
    try {
      const response = await fetch(driftUrls[index], {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ drift_value: driftInputs[index] }),
      });

      if (response.ok) {
        const data = await response.json();
        setStatusMessages(prev => {
          const newMessages = [...prev];
          newMessages[index] = `Drift atualizado com sucesso: ${data.drift_value}`;
          return newMessages;
        });
      } else {
        setStatusMessages(prev => {
          const newMessages = [...prev];
          newMessages[index] = `Erro ao atualizar drift: ${response.statusText}`;
          return newMessages;
        });
      }
    } catch (error) {
      setStatusMessages(prev => {
        const newMessages = [...prev];
        newMessages[index] = `Erro ao enviar requisição: ${error.message}`;
        return newMessages;
      });
    }
  };

  return (
    <div className="py-20">
      <h1 className="heading">
      Other Distributed Clocks{" "}
        <span className="text-purple"></span>
      </h1>
      <div className="flex flex-wrap items-center justify-center p-4 gap-16 mt-10">
        {projects.map((item, index) => (
          <div
            className="lg:min-h-[32.5rem] h-[25rem] flex items-center justify-center sm:w-96 w-[80vw]"
            key={item.id}
          >
            <PinContainer
              title="Clock"
              href={item.link}
            >
              <div className="relative flex items-center justify-center sm:w-96 w-[80vw] overflow-hidden h-[20vh] lg:h-[30vh] mb-10">
                <div
                  className="relative w-full h-full overflow-hidden lg:rounded-3xl"
                  style={{ backgroundColor: "#1e1e1e" }}
                >
                  <Clock apiUrl={apiUrls[index]} />
                </div>
              </div>

              <h1 className="font-bold lg:text-2xl md:text-xl text-base line-clamp-1">
                Clock {index + 1}
              </h1>

              <p
                className="lg:text-xl lg:font-normal font-light text-sm line-clamp-2"
                style={{
                  color: "#BEC1DD",
                  margin: "1vh 0",
                }}
              >
 
              </p>

              <div className="flex items-center justify-between mt-7 mb-3">
                <div className="flex items-center">
                  <input
                    type="text"
                    value={driftInputs[index]}
                    onChange={(event) => handleDriftChange(index, event)}
                    placeholder="Digite o drift..."
                    className="border border-white/[.2] rounded-full bg-black lg:w-40 lg:h-10 w-32 h-8 p-2 text-white"
                  />
                </div>

                <div className="flex justify-center items-center">
                  <p
                    onClick={() => handleDriftUpdate(index)}
                    className="flex lg:text-xl md:text-xs text-sm text-purple cursor-pointer"
                  >
                    Alterar drift
                  </p>
                  <FaLocationArrow className="ms-3" color="#CBACF9" />
                </div>
              </div>

              {statusMessages[index] && (
                <p className={`mt-2 ${statusMessages[index].startsWith('Erro') ? 'text-red-500' : 'text-green-500'}`}>
                  {statusMessages[index]}
                </p>
              )}
            </PinContainer>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecentProjects;
