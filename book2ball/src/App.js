import Navbar from './components/navbar';
import Hero from './components/hero';
import Footer from './components/footer';
import About from './components/about';
import Contact from './components/contact';
import './App.css';

function App() {
  return (
    <div className="App">
      <Navbar />
      <main>
        <Hero />
        <About />
        <Contact />
      </main>
      <Footer />
    </div>
  );
}

export default App;