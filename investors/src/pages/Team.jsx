import { TEAM } from "../content.js";
import Picture from "../Picture.jsx";
import useTitle from "../useTitle.js";

export default function Team() {
  useTitle(TEAM.title);
  return (
    <article className="team">
      <Picture image={TEAM.photo} className="team-photo" />
      <div className="section">
        <h1 className="h1">{TEAM.title}</h1>
        <ul className="members">
          {TEAM.members.map((m, i) => (
            <li className="member" key={i}>
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
            </li>
          ))}
        </ul>
      </div>
    </article>
  );
}
