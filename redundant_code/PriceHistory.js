// this component will display the price history in the dashboard
import React, { useState, useEffect } from "react";
import axios from "axios";

const PriceHistory = () => {
  const [entries, setEntries] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [sortField, setSortField] = useState("created_at");
  const [sortOrder, setSortOrder] = useState("desc");

  useEffect(() => {
    fetchEntries();
  }, [searchTerm, startDate, endDate, page, sortField, sortOrder]);

  const fetchEntries = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/api/price-history/",
        {
          params: {
            search: searchTerm,
            start_date: startDate,
            end_date: endDate,
            page,
            sort: sortField,
            order: sortOrder,
          },
        }
      );
      setEntries(response.data.results);
      setTotalPages(response.data.total_pages);
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  };

  const handleEdit = (index, field, value) => {
    const updatedEntries = [...entries];
    updatedEntries[index][field] = value;
    setEntries(updatedEntries);
  };

  const handleSave = async (entry) => {
    try {
      await axios.put(
        `http://127.0.0.1:8000/api/update-entry/${entry.id}/`,
        entry
      );
      alert("Entry updated successfully!");
    } catch (error) {
      console.error("Error updating entry:", error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/delete-entry/${id}/`);
      setEntries(entries.filter((entry) => entry.id !== id));
    } catch (error) {
      console.error("Error deleting entry:", error);
    }
  };

  const toggleSort = (field) => {
    setSortField(field);
    setSortOrder(sortOrder === "asc" ? "desc" : "asc");
  };

  return (
    <div>
      <h2>Price History</h2>

      {/* Search & Filter Inputs */}
      <input
        type="text"
        placeholder="Search by name..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <input
        type="date"
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
      />
      <input
        type="date"
        value={endDate}
        onChange={(e) => setEndDate(e.target.value)}
      />

      {/* Pagination Buttons */}
      <button disabled={page === 1} onClick={() => setPage(page - 1)}>
        Previous
      </button>
      <span>
        {" "}
        Page {page} of {totalPages}{" "}
      </span>
      <button disabled={page === totalPages} onClick={() => setPage(page + 1)}>
        Next
      </button>

      <table>
        <thead>
          <tr>
            <th onClick={() => toggleSort("created_at")}>
              Date{" "}
              {sortField === "created_at" && (sortOrder === "asc" ? "↑" : "↓")}
            </th>
            <th>Establishment</th>
            <th onClick={() => toggleSort("price")}>
              Price {sortField === "price" && (sortOrder === "asc" ? "↑" : "↓")}
            </th>
            <th>Receipt</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((entry, index) => (
            <tr key={entry.id}>
              <td>{entry.created_at}</td>
              <td>{entry.name}</td>
              <td>£{entry.items.reduce((acc, item) => acc + item.price, 0)}</td>
              <td>
                {entry.uploaded_document ? (
                  <a
                    href={entry.uploaded_document}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View
                  </a>
                ) : (
                  "No Receipt"
                )}
              </td>
              <td>
                <button onClick={() => handleSave(entry)}>Save</button>
                <button onClick={() => handleDelete(entry.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PriceHistory;
