import React, { useState, useEffect } from "react";

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const EXHIBITIONS_API = "https://onunlky5ka.execute-api.eu-central-1.amazonaws.com/prod/exhibitions";
    // Fetch data using the native fetch API
    fetch(EXHIBITIONS_API)
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
            <li key={index}>
              <div><b>Title:</b> {item.title}</div>
              <div>{item.shortdescription}</div>
              <div><b>Location:</b> {item.venues[0].city}</div>
                {item.weather?.forecast.map((weather_condition, index1) => (
                  <div key={index1}>{weather_condition}</div>
                ))}
            </li>  // Render items from API response
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
