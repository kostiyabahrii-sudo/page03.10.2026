import { LINKS, PRODUCTS } from "../content.js";
import Picture from "../Picture.jsx";
import useTitle from "../useTitle.js";

function Copy({ product, href, id }) {
  return (
    <div className="product-copy">
      <h2 className="h1" id={id}>
        {product.name}
      </h2>
      {product.description.map((text, i) => (
        <p className="body" key={i}>
          {text}
        </p>
      ))}
      <a
        className="button"
        href={href}
        target="_blank"
        rel="noopener noreferrer"
      >
        {product.cta}
        <span aria-hidden="true">↗</span>
      </a>
    </div>
  );
}

export default function Products() {
  useTitle(PRODUCTS.title);
  const { extension, app } = PRODUCTS;
  return (
    <article>
      <h1 className="visually-hidden">{PRODUCTS.title}</h1>

      {/* Screen 1: screenshot left, description right */}
      <section className="product" aria-labelledby="p-extension">
        <div className="product-grid">
          <div className="product-media">
            <Picture image={extension.screenshot} className="shot-extension" />
          </div>
          <Copy product={extension} href={LINKS.store} id="p-extension" />
        </div>
        <a className="hint" href="#app">
          {app.name} <span aria-hidden="true">↓</span>
        </a>
      </section>

      {/* Screen 2: description left, two screenshots right */}
      <section className="product" id="app" aria-labelledby="p-app">
        <div className="product-grid">
          <Copy product={app} href={LINKS.waitlist} id="p-app" />
          <div className="product-media shots">
            {app.screenshots.map((shot, i) => (
              <Picture image={shot} className="shot-phone" key={i} />
            ))}
          </div>
        </div>
      </section>
    </article>
  );
}
