
// STILL NEEDS WORKED ON --23 JAN 2025
import React from 'react';

const DeleteAccount = () => {
  const handleDelete = () => {
    alert('Your account has been deleted!');
    // Perform API call to delete account --look up how to do this
  };

  return (
    <div className="delete-account-page">
      <h1>Delete Account</h1>
      <p>Are you sure you want to delete your account? This action cannot be undone.</p>
      <button onClick={handleDelete} className="delete-button">
        Confirm Delete
      </button>
    </div>
  );
};

export default DeleteAccount;
