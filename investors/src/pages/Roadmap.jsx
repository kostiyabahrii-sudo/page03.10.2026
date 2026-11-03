import { FAQ, ROADMAP } from "../content.js";
import useTitle from "../useTitle.js";

export default function Roadmap() {
  useTitle(ROADMAP.title);
  return (
    <article>
      <section className="section roadmap-screen">
        <h1 className="h1">{ROADMAP.title}</h1>

        <ol className="stages">
          {ROADMAP.stages.map((stage) => (
            <li className="stage" key={stage.label}>
              <span className="stage-label">{stage.label}</span>
              <span className="stage-rule" aria-hidden="true" />
              <p className="stage-text">{stage.items.join(", ")}</p>
            </li>
          ))}
        </ol>

        <a className="hint" href="#faq">
          {FAQ.title} <span aria-hidden="true">↓</span>
        </a>
      </section>

      <section className="section narrow faq" id="faq">
        <h2 className="h1">{FAQ.title}</h2>
        <div className="faq-list">
          {FAQ.items.map((item, i) => (
            <details className="faq-item" key={i}>
              <summary>
                <span>{item.q}</span>
                <span className="faq-sign" aria-hidden="true" />
              </summary>
              <p className="body">{item.a}</p>
            </details>
          ))}
        </div>
      </section>
    </article>
  );
}
