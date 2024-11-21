import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { auth } from '../config/firebase';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { useAuth } from '../contexts/AuthContext';
import './login.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      const token = await user.getIdToken(); // Get the JWT from Firebase
      login(token); // Store the JWT using the useAuth hook
      // Redirect to the dashboard
      navigate('/dashboard');
    } catch (error) {
      setError('Failed to log in');
      console.error('Error logging in:', error);
    }
  };

  return (
    <div className="login">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <label htmlFor="email">Email</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          autoComplete='email'
        />
        <label htmlFor="password">Password</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          autoComplete='current-password'
        />
        {error && <p className="error">{error}</p>}
        <button type="submit">LOGIN</button>
        <p>Don't have an account? <a href="/signup">Sign up</a></p>
      </form>
    </div>
  );
}

export default Login;