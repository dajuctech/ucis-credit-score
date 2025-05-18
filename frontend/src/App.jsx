import { useState } from 'react'
import './App.css'

function App() {
  const [features, setFeatures] = useState(Array(18).fill(''))
  const [prediction, setPrediction] = useState(null)

  const handleChange = (index, value) => {
    const newFeatures = [...features]
    newFeatures[index] = value
    setFeatures(newFeatures)
  }

  const handleSubmit = async () => {
    const numericFeatures = features.map(f => parseFloat(f))
    const res = await fetch('http://localhost:8000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ features: numericFeatures }),
    })

    const data = await res.json()
    setPrediction(data.prediction || data.detail)
  }

  return (
    <div className="App">
      <h1>Credit Score Predictor</h1>

      {features.map((val, i) => (
        <input
          key={i}
          type="number"
          placeholder={`Feature ${i + 1}`}
          value={val}
          onChange={(e) => handleChange(i, e.target.value)}
        />
      ))}

      <button onClick={handleSubmit}>Predict</button>

      {prediction && (
        <h2>Prediction: {prediction}</h2>
      )}
    </div>
  )
}

export default App
