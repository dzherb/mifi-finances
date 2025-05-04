

export function isMockApi() {
  return import.meta.env.VITE_API_MOCK === "true"
}