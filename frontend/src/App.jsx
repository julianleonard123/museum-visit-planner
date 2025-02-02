import React, { useState, useEffect } from "react";

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState(""); // Add state for filter criteria
  const EXHIBITIONS_API = "https://onunlky5ka.execute-api.eu-central-1.amazonaws.com/prod/exhibitions";
  const GOOGLE_DIRECTIONS_API = "https://www.google.com/maps/dir/?api=1&destination="
    
  useEffect(() => {
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

  const filteredData = data.filter(item => {
    return item.weather?.forecast[0].toLowerCase().includes(filter.toLowerCase()) ||
      item.weather?.forecast[1]?.toLowerCase().includes(filter.toLowerCase()); // Filter by weather
  });

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-10 px-4">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Exhibitions</h1>

      <div className="mb-6 w-full max-w-3xl">
        <input
          type="text"
          placeholder="Filter by weather"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="w-full p-3 border rounded-lg"
        />
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-40">
          <div className="animate-spin rounded-full h-10 w-10 border-t-4 border-blue-500"></div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-6xl">
          {filteredData.map((item, index) => (
            <div
              key={index}
              className="bg-white p-5 rounded-2xl shadow-lg border border-gray-200"
            >
              <img
                src={item.poster?.imageurl}
              />
              <h2 className="text-xl font-semibold text-gray-700 mb-2">{item.title}</h2>
              <p className="text-gray-600 mb-3">{item.shortdescription}</p>
              <p className="text-sm text-gray-500"><b>Location: </b>
                <a
                  href={`${GOOGLE_DIRECTIONS_API}${encodeURIComponent(item.venues[0].city)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 hover:underline"
                >
                  {item.venues[0].city}
                </a></p>
              <p className="text-sm text-gray-500"><b>End Date: </b>
                  {item.enddate ? new Date(item.enddate).toLocaleDateString("en-US", { day: "numeric", month: "long", year: "numeric" }) : "N/A"}
                </p>
              {item.weather?.forecast.length > 1 && (
                <div className="mt-2">
                  <b className="text-gray-600">Weather Forecast</b>
                  <ul className="text-sm text-gray-500 list-disc pl-5 mt-1">
                    <li>Today: {item.weather?.forecast[0]}</li>
                    <li>Tomorrow: {item.weather?.forecast[1]}</li>
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
