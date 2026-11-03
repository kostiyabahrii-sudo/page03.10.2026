// All site copy, links and images live here. Edit this file to fill the site.
//
// Images: put files into /public and set `src` (e.g. "/team.jpg").
// While `src` is null a labelled placeholder box is shown instead.

export const BRAND = "Fitkit";

export const LINKS = {
  linkedin: "https://www.linkedin.com/company/fitkitcommerce/",
  // Override at build time with VITE_WAITLIST_URL / VITE_STORE_URL.
  waitlist: import.meta.env.VITE_WAITLIST_URL || "#",
  store: import.meta.env.VITE_STORE_URL || "#",
};

export const ABOUT = {
  title: "About",
  lead: "Placeholder. One or two sentences on what Fitkit is and why it matters.",
  paragraphs: [
    "Placeholder text. The problem: describe who struggles with what, and how often.",
    "Placeholder text. The solution: what Fitkit does differently, in plain words.",
    "Placeholder text. Traction and where we are today: users, waitlist size, partners.",
  ],
};

export const TEAM = {
  title: "Team",
  photo: {
    src: null,
    alt: "The Fitkit team",
    placeholder: "Team photo — wide, 16:9",
  },
  members: [
    {
      name: "Name Surname",
      role: "Co-founder, CEO",
      bio: "Placeholder. Background, previous experience, what they own at Fitkit.",
      linkedin: null,
    },
    {
      name: "Name Surname",
      role: "Co-founder, CTO",
      bio: "Placeholder. Background, previous experience, what they own at Fitkit.",
      linkedin: null,
    },
    {
      name: "Name Surname",
      role: "Design",
      bio: "Placeholder. Background, previous experience, what they own at Fitkit.",
      linkedin: null,
    },
  ],
};

export const ROADMAP = {
  title: "Roadmap",
  stages: [
    {
      label: "Now",
      items: ["Finish MVP", "acquire funding", "launch iOS app"],
    },
    {
      label: "Next",
      items: ["Checkout beta", "set up legal entity", "marketing campaign"],
    },
    {
      label: "Later",
      items: [
        "Extend business to non-clothing items",
        "contracts with shipping companies",
        "contracts with vendors",
        "subscription-based creator fees",
        "Android app",
        "worldwide operation",
        "in-house search optimization",
      ],
    },
  ],
};

export const FAQ = {
  title: "FAQ",
  items: [
    {
      q: "Placeholder question: how does Fitkit make money?",
      a: "Placeholder answer.",
    },
    {
      q: "Placeholder question: how much are you raising?",
      a: "Placeholder answer.",
    },
    {
      q: "Placeholder question: who are your competitors?",
      a: "Placeholder answer.",
    },
    {
      q: "Placeholder question: how can I get in touch?",
      a: "Placeholder answer.",
    },
  ],
};

export const PRODUCTS = {
  title: "Products",
  extension: {
    name: "Browser extension",
    description: [
      "Placeholder. What the extension does, in one sentence.",
      "Placeholder. How it works for the user, step by step or in two lines.",
    ],
    cta: "Open in store",
    screenshot: {
      src: null,
      alt: "Fitkit browser extension",
      placeholder: "Extension screenshot",
    },
  },
  app: {
    name: "iOS app",
    description: [
      "Placeholder. What the app does, in one sentence.",
      "Placeholder. What's coming at launch.",
    ],
    cta: "Join waitlist",
    screenshots: [
      { src: null, alt: "Fitkit app, screen 1", placeholder: "App screen 1" },
      { src: null, alt: "Fitkit app, screen 2", placeholder: "App screen 2" },
    ],
  },
};
