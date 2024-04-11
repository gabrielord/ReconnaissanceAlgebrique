import React, { useState } from 'react';
import './App.css'; // Importing CSS file for styling
import { BlockMath } from 'react-katex';

function App() {
  const [equation, setEquation] = useState('');
  const [inputValue, setInputValue] = useState('');
  const [inputValue2, setInputValue2] = useState('');
  const [result, setResult] = useState('');
  const string1 = 'x'; // Define your global variable here

  var Latex = require('react-latex');
  
  function escapeBackslash(inputString) {
    return inputString.replace(/\\/g, "backl");
  }


  // Function to handle submit button click
  const handleSubmit = async () => {
    try {
      // Make GET request to API endpoint
      const response = await fetch(`http://localhost:8000/api/get_score/${escapeBackslash(inputValue)}/${escapeBackslash(inputValue2)}`);
      
      // Check if request was successful
      if (response.ok) {
        // Parse response JSON
        const data = await response.json();
        setResult("Distance: " + data.result[2]);
      } else {
        setResult('Error: Unable to process request');
      }
    } catch (error) {
      setResult('Error: Unable to process request');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Compare Expressions</h1>
        <link
            href="//cdnjs.cloudflare.com/ajax/libs/KaTeX/0.9.0/katex.min.css"
            rel="stylesheet"
        />
      </header>
      <div className="equation">
        {/* <p>Base expression:</p>
        <h3>
                <Latex>$(3\times 4) \div (5-3)$</Latex>
        </h3> */}
      </div>
      <div className="input-container">
      <input
          type="text"
          style={{ marginRight: '10px' }}
          placeholder="Enter your expression"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        />

        <input
          type="text"
          placeholder="Enter your expression"
          value={inputValue2}
          onChange={(e) => setInputValue2(e.target.value)}
        />
      </div>
      <div className="input-container">
        <button onClick={handleSubmit}>Submit</button>
      </div>
      <div className="result">
        <p>{result}</p>
      </div>
    </div>
  );
}

export default App;
