import React, { createContext, useContext, useState, useEffect } from 'react';
import { auth } from '../config/firebase'; // Ensure you have Firebase initialized
import { signOut } from 'firebase/auth';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      if (user) {
        setUser(user); // Store the Firebase user object
      } else {
        setUser(null);
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  // Function to log in the user and store the JWT
  const login = (token) => {
    localStorage.setItem('token', token);
    setUser(auth.currentUser); // Store the Firebase user object
  };

  // Function to log out the user
  const logout = async () => {
    await signOut(auth);
    localStorage.removeItem('token');
    setUser(null);
  };

  // Function to get the JWT
  const getToken = async () => {
    if (user) {
      return await user.getIdToken(); // Use the getIdToken method on the Firebase user object
    }
    return null;
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