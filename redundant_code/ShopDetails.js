//This file was built as part of a design to have individual shop details but wasnt able to be implemented in the time frame

import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "../pages/css sheets/ShopDetails.css";
import Header from "../frontend/src/components/Header";
import Footer1 from "../frontend/src/components/Footer1";

function ShopDetails() {
  const { id } = useParams();
  const [shop, setShop] = useState(null);

  useEffect(() => {
    const fetchShopDetails = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/cafes/${id}/`);
        const data = await response.json();
        setShop(data);
      } catch (error) {
        console.error("Error fetching shop details:", error);
      }
    };

    fetchShopDetails();
  }, [id]);

  if (!shop) {
    return <p>Loading...</p>;
  }

  //---------------------------------------------------------------
// Below is the ShopDetails component which displays the details of a specific shop.
// It fetches the shop details based on the ID from the URL parameters.
// It uses the useEffect hook to fetch the data when the component mounts.
// The fetched data is stored in the shop state variable.
//---------------------------------------------------------------
  return (
    <div className="App">
      <Header />
      <main className="shop-details">
        <div
          className="shop-image"
          style={{
            backgroundImage: `url(${shop.image || "/default-shop.jpg"})`,
          }}
        ></div>

        <div className="shop-content">
          <div className="shop-info">
            <h2>{shop.name}</h2>
            <p>
              <strong>Address:</strong> {shop.address}
            </p>
            <p>
              <strong>Opening Times:</strong>{" "}
              {shop.opening_times || "Not available"}
            </p>
            <p>
              <strong>Features:</strong> {shop.features || "Not available"}
            </p>
            <p>
              <a href={shop.website} target="_blank" rel="noopener noreferrer">
                Visit Website
              </a>
            </p>
            <p>
              <a
                href={shop.social_media}
                target="_blank"
                rel="noopener noreferrer"
              >
                Social Media
              </a>
            </p>
          </div>

          <div className="reviews">
            <h3>Reviews</h3>
            <div className="reviews-container">
              {shop.reviews && shop.reviews.length > 0 ? (
                shop.reviews.map((review, index) => (
                  <div key={index} className="review-card">
                    <p>
                      <strong>{review.user}</strong> - {review.rating}/5
                    </p>
                    <p>{review.comment}</p>
                  </div>
                ))
              ) : (
                <p>No reviews yet.</p>
              )}
            </div>
          </div>
        </div>
      </main>
      <Footer1 />
    </div>
  );
}

export default ShopDetails;
