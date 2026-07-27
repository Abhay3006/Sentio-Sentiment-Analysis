import { Sparkles } from "lucide-react";
import "./Header.css";

function Header({ title, tagline }) {
  const words = title.split(" ");
  const lastWord = words.slice(-1).join(" ");
  const rest = words.slice(0, -1).join(" ");

  return (
    <header className="header">
      <nav className="header-nav">
        <div className="brand">
          <div className="brand-mark">S</div>
          <span>Sentio</span>
        </div>
        <span className="brand-badge">AI · Sentiment Intelligence</span>
      </nav>

      <div className="hero">
        <span className="hero-eyebrow">
          <span className="hero-eyebrow-dot" />
          Powered by machine learning
        </span>
        <h1>
          {rest} <span className="gradient">{lastWord}</span>
        </h1>
        {tagline && <p className="hero-tagline">{tagline}</p>}
      </div>
    </header>
  );
}

export default Header;
