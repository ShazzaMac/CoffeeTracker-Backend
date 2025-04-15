import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

function OCRPreview() {
  const location = useLocation();
  const navigate = useNavigate();

  // Extract OCR-generated data + user manual inputs from the passed location state
  const { extractedData, userInputs } = location.state || {
    extractedData: [],
    userInputs: {},
  };

  // Store editable extracted data
  const [editedData, setEditedData] = useState(extractedData || []);

  // Handle manual changes
  const handleChange = (index, key, value) => {
    const updatedData = [...editedData];
    updatedData[index][key] = value;
    setEditedData(updatedData);
  };

  // Handle form submission (save to database)
  const handleSubmit = async () => {
    const finalData = {
      extractedData: editedData,
      userInputs: userInputs, // Include manual inputs (checkboxes, ratings, etc.)
    };

    const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)?.[1]; // Extract CSRF token from cookies

    try {
      await axios.post(
        "http://127.0.0.1:8000/api/save-extracted-data/",
        finalData,
        {
          headers: {
            "X-CSRFToken": csrfToken, // Attach CSRF token
          },
        }
      );
      alert("Data saved successfully!");
      navigate("/"); // Redirect to home after saving
    } catch (error) {
      console.error("Save error:", error);
      alert("Failed to save data.");
    }
  };

  return (
    <div>
      <h2>Review & Edit Extracted Data</h2>
    {editedData.length > 0 ? (
        editedData.map((item, index) => (
          <div key={index}>
            <label>
              Title:
              <input
                type="text"
                value={item.title}
                onChange={(e) => handleChange(index, "title", e.target.value)}
              />
            </label>
            <label>
              Description:
              <input
                type="text"
                value={item.description}
                onChange={(e) =>
                  handleChange(index, "description", e.target.value)
                }
              />
            </label>
            <label>
              Price:
              <input
                type="text"
                value={item.price}
                onChange={(e) => handleChange(index, "price", e.target.value)}
              />
            </label>
          </div>
        ))
      ) : (
        <p>No extracted data available.</p>
      )}

      <button onClick={handleSubmit}>Confirm & Save</button>
    </div>
  );
}

export default OCRPreview;
