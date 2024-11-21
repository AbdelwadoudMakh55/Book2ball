import { createContext, useState, useContext, useEffect } from 'react';
import { auth } from '../config/firebase';
import { onAuthStateChanged, signOut } from 'firebase/auth';

// Create the AuthContext
const AuthContext = createContext();

// Create the AuthProvider component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Listen for authentication state changes
  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });

    // Cleanup subscription on unmount
    return () => unsubscribe();
  }, []);

  // Function to log in the user and store the JWT
  const login = (token) => {
    localStorage.setItem('token', token);
    setUser({ token });
  };

  // Function to log out the user
  const logout = async () => {
    await signOut(auth);
    localStorage.removeItem('token');
    setUser(null);
  };

  // Function to get the JWT
  const getToken = () => {
    return localStorage.getItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading, getToken }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the AuthContext
export const useAuth = () => {
  return useContext(AuthContext);
};