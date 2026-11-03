import { Link } from "react-router-dom";
import { ABOUT } from "../content.js";
import useTitle from "../useTitle.js";

export default function About() {
  useTitle(null);
  return (
    <article className="section narrow">
      <h1 className="h1">{ABOUT.title}</h1>
      <p className="lead">{ABOUT.lead}</p>
      {ABOUT.paragraphs.map((text, i) => (
        <p className="body" key={i}>
          {text}
        </p>
      ))}
      <nav className="next" aria-label="Continue">
        <Link to="/roadmap">Roadmap →</Link>
        <Link to="/products">Products →</Link>
      </nav>
    </article>
  );
}
