import React, { useState, useEffect } from "react";

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data using the native fetch API
    fetch("https://ug5u8avkf7.execute-api.eu-central-1.amazonaws.com/prod/exhibitions")
      .then((response) => response.json())
      .then((data) => {
        setData(data);  // Update state with fetched data
        setLoading(false);  // Set loading to false once data is fetched
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false);
      });
  }, []);  // Run once when the component mounts

  return (
    <div className="App">
      <h1>Exhibitions</h1>

      {loading ? (
        <p>Loading...</p>  // Display a loading message
      ) : (
        <ul>
          {data.map((item, index) => (
            <li key={index}>{item.name} {item.city}</li>  // Render items from API response
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
