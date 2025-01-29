import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { Amplify } from "aws-amplify";

// Amplify.configure({
//   API: {
//     endpoints: [
//       {
//         name: "exhibitionsApi", // Reference name
//         endpoint: "https://ug5u8avkf7.execute-api.eu-central-1.amazonaws.com/prod/", 
//         region: "eu-central-1",
//       },
//     ],
//   },
// });

// async function fetchData() {
//   try {
//     const response = await API.get("exhibitionsApi", "/exhibitions");
//     console.log("Data:", response);
//   } catch (error) {
//     console.error("Error fetching data:", error);
//   }
// }


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
