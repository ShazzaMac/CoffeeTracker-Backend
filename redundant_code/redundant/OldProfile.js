import React, { useState, useEffect, useContext } from "react"; // Import the hooks which are needed to build the component
import AuthContext from "../../frontend/src/hooks/AuthContext"; // Authenticated context for managing user login state
import Header from "../../frontend/src/components/Header";
import Footer1 from "../../frontend/src/components/Footer1";
import "../pages/css sheets/Profile.css";


//Profile component
const Profile = () => {
  // Destructure the token and login/logout functions from the AuthContext
  const { token, login, logout } = useContext(AuthContext); // Destructure the token and login/logout functions from the AuthContext

  //state variables for the profile page
  const [profilePhoto, setProfilePhoto] = useState(null);
  const [userName, setUserName] = useState(""); // New state to hold the username
  const [errorMessage, setErrorMessage] = useState("");
  const [updateSuccess, setUpdateSuccess] = useState("");
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    phone: "",
    about: "",
  });
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [userBadges, setUserBadges] = useState(["🚀", "🎉"]);
  const [showPassword, setShowPassword] = useState(false);
  const [password, setPassword] = useState({
    currentPassword: "",
    newPassword: "",
    confirmNewPassword: "",
  });
  const [passwordError, setPasswordError] = useState("");
  const [passwordSuccess, setPasswordSuccess] = useState("");

  //fetching the profile data when the component mounts or the token changes
  useEffect(() => {
    if (!token) return;

    const fetchProfileData = async () => {
        try {
            const response = await fetch("/api/accounts/profile/", {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            
            if (response.ok) {
                const data = await response.json();
                console.log("Profile data:", data); // Debugging log
                setFormData({
                    username: data.username,
                    email: data.email || "",
                    phone: data.phone || "",
                    about: data.about || "",
                });
                setProfilePhoto(data.profilePhoto);
            } else {
                setErrorMessage("Failed to fetch profile data");
            }
        } catch (error) {
            console.error("Failed to fetch profile data", error);
        }
    };

    fetchProfileData(); // ✅ Now correctly calls the function
}, [token]);

//-----------------------------------Upload photo function-----------------------------------

//
  const handlePhotoUpload = (e) => {
    const file = e.target.files[0];

    if (!file) {
      console.error("No file selected");
      return;
    }

    const validTypes = ["image/jpeg", "image/png"];

    if(!validTypes.includes(file.type)){
      setErrorMessage("Only JPEG and PNG images are allowed.");
      return;
    }

    if (file.size <= 5 * 1024 * 1024) {
      setProfilePhoto(URL.createObjectURL(file));
      setErrorMessage("");
      console.log("Profile photo:", file.type); // Debugging log
    } else {
      setProfilePhoto(null);
      setErrorMessage("Only JPEG and PNG images under 5MB are allowed.");
    }
  };

//-----------------------------------Upload photo function-----------------------------------

const uploadPhoto = async () => {
  if (!profilePhoto) {
    console.error("No file selected");
    return;
  }

  const photoData = new FormData();
  photoData.append("photo", profilePhoto); // Make sure you're appending the file, not URL

  try {
    const response = await fetch("http://localhost:8000/api/accounts/profile/upload-photo/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: photoData,
    });

    if (response.ok) {
      console.log("Profile photo uploaded successfully");
    } else {
      setErrorMessage("Failed to upload profile photo");
    }
  } catch (error) {
    console.error("Failed to upload profile photo", error);
    setErrorMessage("Failed to upload profile photo");
  }
};


  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPassword({ ...password, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formDataToSend = { ...formData };
    delete formDataToSend.profilePhoto; // Ensure profile photo isn't sent in this request
  
    console.log("Submitting profile update:", formDataToSend); // Debugging log
  
    const response = await fetch("/api/accounts/profile/update", {
      method: "PATCH", // Change from POST to PATCH
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });
    

    setLoading(false);

    if (response.ok) {
      setUpdateSuccess("Settings updated successfully!");
      setIsEditing(false);
    } else {
      setErrorMessage("Failed to update profile");
    }
  };

  useEffect(() => {
    if(profilePhoto && typeof profilePhoto !== "string"){
      const objectUrl = URL.createObjectURL(profilePhoto);
      return () => URL.revokeObjectURL(objectUrl);
    }
  }, [profilePhoto]);

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();

    if (password.newPassword !== password.confirmNewPassword) {
      setPasswordError("Passwords do not match");
      return;
    }

    const response = await fetch("/api/accounts/profile/change-password/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(password),
    });

    if (response.ok) {
      setPasswordSuccess("Password changed successfully!");
      setPassword({
        currentPassword: "",
        newPassword: "",
        confirmNewPassword: "",
      });
      setPasswordError("");
    } else {
      setPasswordError("Error changing password");
    }
  };

  const toggleEdit = () => {
    setIsEditing(!isEditing);
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };
  return (
    <div className="settings-page">
      <Header />
      <div className="settings-container">
        <h1>Profile Settings</h1>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        {updateSuccess && <p className="success-message">{updateSuccess}</p>}
        {loading && <p className="loading-message">Updating profile...</p>}

        <p className="subheader">
          Manage your personal information and profile settings below
        </p>
        <div className="welcome-message">
          <h2>Welcome, {formData.username}!</h2>
        </div>

{/* Profile photo upload section */}
        <div className="form-section photo-upload">
          <h1>Profile Photo</h1>
          <div className="preview">
  {profilePhoto ? (
    <img
      src={
        typeof profilePhoto === "string"
          ? profilePhoto.startsWith("blob:")
            ? profilePhoto
            : `/media/${profilePhoto}`
          : URL.createObjectURL(profilePhoto)
      }
      alt="Preview"
    />
  ) : (
    <div className="placeholder">No Image Uploaded</div>
  )}
</div>

          <input
            type="file"
            accept=".jpg,.jpeg,.png"
            onChange={handlePhotoUpload}
            className="file-input"
            disabled={!isEditing}
          />
           <button 
    onClick={uploadPhoto} 
    className="upload-button" 
    disabled={!profilePhoto || !isEditing}
  >
    Upload Photo
  </button>
  <small>Only JPEG and PNG images under 5MB are allowed</small>
  {errorMessage && <p className="error-message">{errorMessage}</p>}
</div>

{/* User information section */}
        <div className="settings-content">
          <div className="profile-left">
            <h3>User Information</h3>
            <form onSubmit={handleSubmit} className="settings-form">
              <div className="form-section">
                <h3>Basic Info</h3>
                <label>Username</label>
                <input
                  type="text"
                  name="username"
                  placeholder="username"
                  value={formData.username}
                  onChange={handleInputChange}
                  className="input-field"
                  disabled={!isEditing}
                />
                <label>Email</label>
                <input
                  type="email"
                  name="email"
                  placeholder="Email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="input-field"
                  disabled={!isEditing}
                />
                <label>Phone</label>
                <input
                  type="tel"
                  name="phone"
                  placeholder="Phone Number"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="input-field"
                  disabled={!isEditing}
                />
                <label>About Me</label>
                <textarea
                  name="about"
                  placeholder="Tell us a bit about yourself..."
                  value={formData.about}
                  onChange={handleInputChange}
                  className="textarea-field"
                  disabled={!isEditing}
                ></textarea>
              </div>
              {isEditing && (
                <button type="submit" className="update-button">
                  Update Profile
                </button>
              )}
            </form>
            <button onClick={toggleEdit} className="edit-button">
              {isEditing ? "Cancel Edit" : "Edit Profile"}
            </button>
          </div>

          <div className="profile-right">
            <h3>My Favourite Places are:</h3>
            <ul className="favourites-list">
              <li>🧑‍💻 Place 1</li>
              <li>📚 Place 2</li>
              <li>🎮 Place 3</li>
            </ul>

            <h3>User Badges</h3>
            <div className="badges">
              {userBadges.map((badge, index) => (
                <span key={index} className="badge">
                  {badge}
                </span>
              ))}
            </div>
            <br />
            <h3>Password Change</h3>
            <button
              onClick={togglePasswordVisibility}
              className="password-button"
            >
              {showPassword ? "Hide Password" : "Show Password"}
            </button>
            {showPassword && (
              <div className="password-section">
                <form onSubmit={handlePasswordSubmit} className="password-form">
                  <label>Current Password</label>
                  <input
                    type="password"
                    name="currentPassword"
                    placeholder="Current Password"
                    className="input-field"
                    value={password.currentPassword}
                    onChange={handlePasswordChange}
                    disabled={!isEditing}
                  />
                  <label>New Password</label>
                  <input
                    type="password"
                    name="newPassword"
                    placeholder="New Password"
                    className="input-field"
                    value={password.newPassword}
                    onChange={handlePasswordChange}
                    disabled={!isEditing}
                  />

                  <label>Confirm New Password</label>
                  <input
                    type="password"
                    name="confirmNewPassword"
                    placeholder="Confirm New Password"
                    className="input-field"
                    value={password.confirmNewPassword}
                    onChange={handlePasswordChange}
                    disabled={!isEditing}
                  />

                  <button type="submit" className="update-button">
                    Change Password
                  </button>
                </form>
              </div>
            )}
          </div>
        </div>
      </div>

      <Footer1 />
    </div>
  );
};

export default Profile;
