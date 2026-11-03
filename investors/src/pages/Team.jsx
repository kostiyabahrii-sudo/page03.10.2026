import { TEAM } from "../content.js";
import Picture from "../Picture.jsx";
import useTitle from "../useTitle.js";

export default function Team() {
  useTitle("Team");
  return (
    <article className="team">
      {TEAM.photo.src && <Picture image={TEAM.photo} className="team-photo" />}
      <div className="section">
        <h1 className="h1">{TEAM.title}</h1>
        <ul className="members">
          {TEAM.members.map((m) => (
            <li className="member" key={m.name}>
              {m.photo ? (
                <img
                  className="portrait"
                  src={m.photo}
                  alt={m.name}
                  loading="lazy"
                />
              ) : (
                <div className="portrait pic-empty" aria-hidden="true" />
              )}
              <div className="member-text">
                <h2 className="h2">{m.name}</h2>
                <p className="role">{m.role}</p>
                <p className="body">{m.bio}</p>
                {m.linkedin && (
                  <a
                    className="text-link"
                    href={m.linkedin}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    LinkedIn ↗
                  </a>
                )}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </article>
  );
}
