import { useEffect } from "react";
import { BRAND } from "./content.js";

export default function useTitle(title) {
  useEffect(() => {
    document.title = title ? `${title} · ${BRAND}` : BRAND;
  }, [title]);
}
