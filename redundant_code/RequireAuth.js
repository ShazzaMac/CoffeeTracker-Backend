// originally this file was intended to be used for authentication and preventing
// unauthorized access to certain routes. It was later decided to use the AuthContext
// to handle authentication and authorization instead. 
import { useContext } from "react";
import { Navigate } from "react-router-dom";
import AuthContext from "../frontend/src/hooks/AuthContext";

const RequireAuth = ({ children }) => {
  const { authTokens } = useContext(AuthContext);

  if (!authTokens || !authTokens.access) {
    return <Navigate to="/login" replace />;
  }

  return children;

};

export default RequireAuth;
