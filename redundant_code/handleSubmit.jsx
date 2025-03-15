// utils/handleSubmit.js
import axios from '../frontend/src/axiosConfig';

export const getCsrfToken = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/csrf/", {
      withCredentials: true,
    });
    return response.data.csrfToken;
  } catch (error) {
    console.error("Failed to get CSRF token:", error);
    return null;
  }
};

const handleSubmit = async (e, file, formData, navigate) => {
  e.preventDefault();
  const csrfToken = await getCsrfToken();
  if (!csrfToken) return;

  const data = new FormData();
  data.append("csrfmiddlewaretoken", csrfToken);
  data.append("file", file);
  Object.keys(formData).forEach((key) => {
    if (typeof formData[key] === "object") {
      Object.keys(formData[key]).forEach((subKey) => {
        data.append(`${key}.${subKey}`, formData[key][subKey]);
      });
    } else {
      data.append(key, formData[key]);
    }
  });

  try {
    await axios.post("/api/submit-price/", data, {
      headers: { "X-CSRFToken": csrfToken },
    });
    navigate("/success");
  } catch (error) {
    console.error("Submission failed:", error);
  }
};

export default handleSubmit;
