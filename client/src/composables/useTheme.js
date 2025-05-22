// composables/useTheme.js
export function useTheme() {
  const applyTheme = (mode) => {
    const root = document.documentElement;

    if (mode === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
  };

  const initTheme = () => {
    // берём mode из userData в localStorage
    const userData = JSON.parse(localStorage.getItem("userData")) || {};
    const savedMode = userData.mode || "light";
    applyTheme(savedMode);
  };

  return { applyTheme, initTheme };
}