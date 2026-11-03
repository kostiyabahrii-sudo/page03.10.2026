// Shows the real image once `src` is set in content.js, otherwise a labelled box.
export default function Picture({ image, className = "" }) {
  if (image.src) {
    return (
      <img className={`pic ${className}`} src={image.src} alt={image.alt} />
    );
  }
  return (
    <div className={`pic pic-empty ${className}`} role="img" aria-label={image.alt}>
      <span>{image.placeholder}</span>
    </div>
  );
}
