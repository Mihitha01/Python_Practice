import React, { useState } from "react";

function App() {
  const [formData, setFormData] = useState({
    Pregnancies: "",
    Glucose: "",
    BloodPressure: "",
    SkinThickness: "",
    Insulin: "",
    BMI: "",
    DiabetesPedigreeFunction: "",
    Age: ""
  });

  const [prediction, setPrediction] = useState(null);

  // Handle input change
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Handle submit
  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        Pregnancies: Number(formData.Pregnancies),
        Glucose: Number(formData.Glucose),
        BloodPressure: Number(formData.BloodPressure),
        SkinThickness: Number(formData.SkinThickness),
        Insulin: Number(formData.Insulin),
        BMI: Number(formData.BMI),
        DiabetesPedigreeFunction: Number(formData.DiabetesPedigreeFunction),
        Age: Number(formData.Age)
      })
    });

    const data = await response.json();
    setPrediction(data.prediction);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Diabetes Prediction</h1>

      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map((key) => (
          <div key={key}>
            <label>{key}: </label>
            <input
              type="number"
              name={key}
              value={formData[key]}
              onChange={handleChange}
              required
            />
          </div>
        ))}

        <button type="submit">Predict</button>
      </form>

      {prediction !== null && (
        <h2>
          Result: {prediction === 1 ? "Diabetes ⚠️" : "No Diabetes ✅"}
        </h2>
      )}
    </div>
  );
}

export default App;