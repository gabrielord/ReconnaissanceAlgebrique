import React, { useRef } from 'react';
import './App.css';
import Header from '../components/Header';

function App() {

  const firstEquationRef = useRef(null);
  const secondEquationRef = useRef(null);

  const checkSimilarity = (event: { preventDefault: () => void; }) => {
    console.log("hty");
    event.preventDefault();


    const data = {
      firstEquation: firstEquationRef.current,
      secondEquation: secondEquationRef.current
    };

    fetch('https://your-backend-api.com/endpoint', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(responseData => {
        console.log('Response from server:', responseData);
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      });
  };

  return (
    <div>
      <Header />
      <div className="App">

        <form className="form" onSubmit={checkSimilarity}>
          <input ref={firstEquationRef} name="first-equation" className="input-field"></input>
          <input ref={secondEquationRef} name="second-equation" className="input-field"></input>
          <button type="submit" className="submit-button">Similarity</button>
        </form>

      </div>
    </div>
  );
}

export default App;
