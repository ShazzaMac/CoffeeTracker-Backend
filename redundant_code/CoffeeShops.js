//---------------------------------------------------------
// This component fetches coffee shop data from the backend API and filters it based on user input.
// It uses the fhrs API to get the list of coffee shops and their details.
// The component also extracts unique postcode prefixes from the addresses of the coffee shops.
//---------------------------------------------------------
import React, { useState, useEffect } from "react";

function CoffeeShops({ rating, postcode, name }) {
  const [coffeeShops, setCoffeeShops] = useState([]);

  useEffect(() => {
    const fetchCoffeeShops = async () => {
      const response = await fetch("http://127.0.0.1:8000/api/cafes/");
      const data = await response.json();
      setCoffeeShops(data);
    };
    fetchCoffeeShops();
  }, []);

  //---------------------------------------------------------

  // Extracts postcode prefixes (e.g., BT1, BT20) from addresses
  const extractPostcodePrefixes = (shops) => {
    const prefixes = new Set(); // Use a Set to store unique prefixes
    shops.forEach((shop) => {
      if (shop.address) {
        const match = shop.address.match(/\b(BT\d{1,2})\b/i); // Match "BT" + 1-2 digits as a separate word
        // \b ensures that "BT" is at the start of a word
        // \d{1,2} matches 1 or 2 digits after "BT"
        // i makes the regex case-insensitive just in case
        if (match) {
          prefixes.add(match[0].toUpperCase()); // Store unique BT codes in uppercase
        }
      }
    });
    return Array.from(prefixes).sort(); // Convert to sorted array
  };

  //---------------------------------------------------------
  //Filter section
  // Filter coffee shops by rating, postcode, and name
  const filteredShops = coffeeShops.filter((shop) => {
    const matchesRating = rating ? shop.rating === rating : true;

    // Extract the shop's postcode prefix (BT1, BT20, etc.)
    const shopPostcodeMatch = shop.address.match(/\b(BT\d{1,2})\b/i);
    const shopPostcode = shopPostcodeMatch
      ? shopPostcodeMatch[0].toUpperCase()
      : "";

    // Ensure exact match for postcode filter
    const matchesPostcode = postcode
      ? shopPostcode === postcode.toUpperCase()
      : true;

    const matchesName = name
      ? shop.name.toLowerCase().includes(name.toLowerCase())
      : true;

    return matchesRating && matchesPostcode && matchesName;
  });

  //---------------------------------------------------------

  return (
    <div className="coffee-shop-list">
      <ul>
        {filteredShops.length > 0 ? (
          filteredShops.map((shop) => (
            <li key={shop.id}>
              <h3>{shop.name}</h3>
              <p>{shop.address}</p>
              <p>Rating: {shop.rating}</p>
            </li>
          ))
        ) : (
          <p>No coffee shops found matching your filters.</p>
        )}
      </ul>
    </div>
  );
}

export default CoffeeShops;
