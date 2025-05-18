import { useState } from "react";
import "./App.css";

function App() {
  const [features, setFeatures] = useState(Array(18).fill(''));
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (index, value) => {
    const updatedFeatures = [...features];
    updatedFeatures[index] = value;
    setFeatures(updatedFeatures);
  };

  const handleSubmit = async () => {
    setError(null);
    try {
      // Convert all inputs to numbers
      const numericFeatures = features.map(f => parseFloat(f));
      
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ features: numericFeatures }),
      });
      if (!response.ok) {
        const errData = await response.json();
        setError(errData.detail || "Prediction error");
        return;
      }
      const data = await response.json();
      setPrediction(data.prediction);
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="App" style={{ padding: "2rem" }}>
      <h1>Credit Score Predictor</h1>
      <p>Enter 18 feature values:</p>
      {features.map((val, i) => (
        <input
          key={i}
          type="number"
          value={val}
          onChange={(e) => handleChange(i, e.target.value)}
          style={{ width: "80px", margin: "5px" }}
        />
      ))}
      <div>
        <button onClick={handleSubmit}>Predict</button>
      </div>
      {prediction && <h2>Prediction: {prediction}</h2>}
      {error && <h3 style={{ color: "red" }}>Error: {error}</h3>}
    </div>
  );
}

export default App;
