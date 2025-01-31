import React, { useState, useEffect } from "react";

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const EXHIBITIONS_API = "https://onunlky5ka.execute-api.eu-central-1.amazonaws.com/prod/exhibitions";
    fetch(EXHIBITIONS_API)
      .then((response) => response.json())
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-10 px-4">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Exhibitions</h1>
      {loading ? (
        <div className="flex justify-center items-center h-40">
          <div className="animate-spin rounded-full h-10 w-10 border-t-4 border-blue-500"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-6xl">
          {data.map((item, index) => (
            <div
              key={index}
              className="bg-white p-5 rounded-2xl shadow-lg border border-gray-200"
            >
              <h2 className="text-xl font-semibold text-gray-700 mb-2">{item.title}</h2>
              <p className="text-gray-600 mb-3">{item.shortdescription}</p>
              <p className="text-sm text-gray-500"><b>Location:</b> {item.venues[0].city}</p>
              {item.weather?.forecast.length > 0 && (
                <div className="mt-2">
                  <b className="text-gray-600">Weather Forecast:</b>
                  <ul className="text-sm text-gray-500 list-disc pl-5 mt-1">
                    {item.weather.forecast.map((condition, index1) => (
                      <li key={index1}>{condition}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
