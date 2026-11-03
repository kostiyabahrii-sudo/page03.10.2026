import { useEffect } from "react";
import { Navigate, NavLink, Route, Routes, useLocation } from "react-router-dom";
import { BRAND, LINKS } from "./content.js";
import About from "./pages/About.jsx";
import Team from "./pages/Team.jsx";
import Roadmap from "./pages/Roadmap.jsx";
import Products from "./pages/Products.jsx";

// Order matches the nav: About | Team | Roadmap | LinkedIn | Products
const NAV = [
  { label: "About", to: "/" },
  { label: "Team", to: "/team" },
  { label: "Roadmap", to: "/roadmap" },
  { label: "LinkedIn", href: LINKS.linkedin },
  { label: "Products", to: "/products" },
];

// Router keeps the old scroll position between pages; reset it unless the
// URL points at an anchor (e.g. /roadmap#faq).
function useScrollReset() {
  const { pathname, hash } = useLocation();
  useEffect(() => {
    if (hash) {
      document.getElementById(hash.slice(1))?.scrollIntoView();
    } else {
      window.scrollTo(0, 0);
    }
  }, [pathname, hash]);
}

export default function App() {
  useScrollReset();

  return (
    <>
      <header className="top">
        <NavLink to="/" className="brand" aria-label={`${BRAND} home`}>
          <img src="/favicon.svg" alt="" width="22" height="22" />
          <span>{BRAND}</span>
        </NavLink>

        <nav className="nav" aria-label="Main">
          {NAV.map((item, i) => (
            <span className="nav-item" key={item.label}>
              {i > 0 && (
                <span className="sep" aria-hidden="true">
                  |
                </span>
              )}
              {item.href ? (
                <a href={item.href} target="_blank" rel="noopener noreferrer">
                  {item.label}
                  <span className="ext" aria-hidden="true">
                    ↗
                  </span>
                </a>
              ) : (
                <NavLink to={item.to} end>
                  {item.label}
                </NavLink>
              )}
            </span>
          ))}
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<About />} />
          <Route path="/about" element={<Navigate to="/" replace />} />
          <Route path="/team" element={<Team />} />
          <Route path="/roadmap" element={<Roadmap />} />
          <Route path="/products" element={<Products />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>

      <footer className="foot">
        <span>
          © {new Date().getFullYear()} {BRAND}
        </span>
        <a href={LINKS.linkedin} target="_blank" rel="noopener noreferrer">
          LinkedIn ↗
        </a>
      </footer>
    </>
  );
}
